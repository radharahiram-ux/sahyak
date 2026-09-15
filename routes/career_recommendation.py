# Career Growth Recommendation Blueprint
import os
import json
import requests
from flask import Blueprint, render_template, request, jsonify

career_bp = Blueprint('career', __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'career_paths.json')

def load_career_paths():
    """Load static career path dataset"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading career paths: {e}")
        return []

def find_best_recommendation(occupation):
    """
    Rule-based lookup engine to find matching career path for an occupation.
    """
    paths = load_career_paths()
    if not paths:
        return None

    norm_occ = (occupation or "").strip().lower()
    
    # 1. Exact match
    for path in paths:
        if path.get("current_occupation", "").lower() == norm_occ:
            return path
            
    # 2. Substring match
    for path in paths:
        curr = path.get("current_occupation", "").lower()
        if norm_occ in curr or curr in norm_occ:
            return path

    return None

def resolve_location_demand(location_input, demand_dict):
    """Resolve location demand (High, Medium, Low) based on region"""
    if not demand_dict:
        return "Medium"
        
    loc = (location_input or "").strip().lower()
    
    if any(k in loc for k in ["urban", "city", "metro", "capital", "delhi", "mumbai", "raipur", "bangalore"]):
        region_key = "urban"
    elif any(k in loc for k in ["rural", "village", "gram", "town"]):
        region_key = "rural"
    else:
        region_key = "default"
        
    demand = demand_dict.get(region_key, demand_dict.get("default", "medium"))
    return demand.capitalize()

def generate_gemini_explanation(current_occupation, current_income, income_goal, experience_years, user_skills, recommended_career, income_min, income_max, skill_gap, location_demand, income_goal_met, training_cost, duration_weeks):
    """
    Calls Gemini API server-side to generate a natural-language explanation
    of why this recommendation makes sense for this specific user.
    Never exposes API key to the frontend.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    gap_str = ", ".join(skill_gap) if skill_gap else "minor advanced techniques"
    user_skills_str = ", ".join(user_skills) if user_skills else "general practical experience"
    
    fallback_text = (
        f"Transitioning from {current_occupation} to {recommended_career} is an ideal career step based on your "
        f"{experience_years} years of background. By bridging the skill gap in {gap_str} through a "
        f"{duration_weeks}-week training costing ₹{training_cost:,}, you position yourself for monthly earnings between "
        f"₹{income_min:,} and ₹{income_max:,}. Job demand in your area is currently {location_demand}, "
        f"{'aligning well with your income goal of ₹' + str(int(income_goal)) + '/month.' if income_goal_met else 'providing strong earning growth towards your income goal.'}"
    )

    if not api_key or api_key == "your_gemini_api_key_here":
        return fallback_text

    prompt = (
        f"You are an expert vocational career advisor. Explain why this pre-computed career recommendation makes sense for this user.\n\n"
        f"User Details:\n"
        f"- Current Occupation: {current_occupation}\n"
        f"- Experience: {experience_years} years\n"
        f"- Current Skills: {user_skills_str}\n"
        f"- Current Monthly Income: ₹{current_income}\n"
        f"- Income Goal: ₹{income_goal}/month\n"
        f"- Location Demand: {location_demand}\n\n"
        f"Recommendation Details:\n"
        f"- Recommended Career: {recommended_career}\n"
        f"- Expected Income Range: ₹{income_min} - ₹{income_max}/month\n"
        f"- Skill Gap to Bridge: {gap_str}\n"
        f"- Training Duration: {duration_weeks} weeks, Cost: ₹{training_cost}\n"
        f"- Income Goal Met: {'Yes' if income_goal_met else 'Partial (may require advanced certifications to reach target)'}\n\n"
        f"Please write a supportive, personalized 2-paragraph explanation highlighting how their current experience accelerates "
        f"their transition, why bridging the skill gap is worth the investment, and how local demand supports their growth. "
        f"Do NOT change or invent a new recommendation; explain only the given recommendation."
    )

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=8)
        
        if response.status_code == 200:
            res_data = response.json()
            candidates = res_data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        else:
            # Fallback to gemini-1.5-flash
            url15 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            response15 = requests.post(url15, json=payload, headers=headers, timeout=8)
            if response15.status_code == 200:
                res_data = response15.json()
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
                        
    except Exception as e:
        print(f"Gemini API call failed or timed out: {e}")

    return fallback_text

@career_bp.route("/career-growth")
def career_growth_page():
    """Render the Career Growth Dashboard page"""
    paths = load_career_paths()
    occupations = [p["current_occupation"] for p in paths]
    return render_template("career_growth.html", occupations=occupations)

@career_bp.route("/api/career-recommendation", methods=["POST"])
def career_recommendation_api():
    """
    API endpoint accepting:
    { occupation, skills, experience_years, location, income_goal, current_income }
    Returns computed recommendation according to 6-stage priority logic.
    """
    try:
        data = request.get_json() or {}
        
        occupation = data.get("occupation", "").strip()
        skills_input = data.get("skills", [])
        experience_years = float(data.get("experience_years", 0))
        location = data.get("location", "").strip()
        income_goal = float(data.get("income_goal", 0))
        current_income = float(data.get("current_income", 20000))
        
        # Validation
        if not occupation:
            return jsonify({"available": False, "error": "Occupation is required"}), 400

        # Parse user skills
        if isinstance(skills_input, str):
            user_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        else:
            user_skills = [str(s).strip() for s in skills_input if str(s).strip()]

        # 1. Occupation lookup
        rec = find_best_recommendation(occupation)
        if not rec:
            return jsonify({
                "available": False,
                "current_occupation": occupation,
                "message": f"No recommendation available yet for '{occupation}'. Try roles like Electrician, Delivery worker, Plumber, Tailor, Construction worker, Driver, or Mechanic."
            }), 200

        required_skills = rec.get("required_skills", [])
        min_exp = rec.get("min_experience_years", 1)
        expected_min = rec.get("expected_income_min", 35000)
        expected_max = rec.get("expected_income_max", 55000)
        base_cost = rec.get("training_cost", 10000)
        base_duration = rec.get("training_duration_weeks", 6)
        available_jobs = rec.get("available_job_titles", [])
        recommended_career = rec.get("recommended_career", "Advanced Specialist")

        # 2. Skill overlap vs skill gap calculation
        user_skills_lower = [s.lower() for s in user_skills]
        skill_overlap = []
        skill_gap = []

        for req in required_skills:
            req_lower = req.lower()
            if any(u in req_lower or req_lower in u for u in user_skills_lower):
                skill_overlap.append(req)
            else:
                skill_gap.append(req)

        # 3. Experience discount logic
        # If experience >= min_experience_years, note reduced training duration/cost (-20%)
        if experience_years >= min_exp:
            experience_discount_applied = True
            training_cost = int(round(base_cost * 0.8))
            training_duration_weeks = round(base_duration * 0.8, 1)
            duration_text = f"{training_duration_weeks} weeks (-20% exp discount)"
        else:
            experience_discount_applied = False
            training_cost = base_cost
            training_duration_weeks = base_duration
            duration_text = f"{training_duration_weeks} weeks"

        # 4. Location demand resolution
        local_demand_dict = rec.get("local_demand_by_region", {})
        local_job_demand = resolve_location_demand(location, local_demand_dict)

        # 5. Income goal evaluation
        income_goal_met = (expected_max >= income_goal) if income_goal > 0 else True
        if not income_goal_met:
            income_goal_note = f"Expected income (max ₹{expected_max:,}) is below your goal of ₹{int(income_goal):,}. Additional senior certifications may be needed."
        else:
            income_goal_note = "Expected income range satisfies your monthly goal."

        # 6. ROI & Payback calculation
        # Formula: roi = ((expected_income_min - current_income) * 12 - training_cost) / training_cost
        monthly_gain = max(1.0, expected_min - current_income)
        net_first_year_gain = (monthly_gain * 12) - training_cost
        estimated_roi = round(net_first_year_gain / training_cost, 2) if training_cost > 0 else 0.0
        payback_period_months = round(training_cost / monthly_gain, 1) if monthly_gain > 0 else 0.0

        # 7. Gemini Explanation (server-side)
        ai_explanation = generate_gemini_explanation(
            current_occupation=occupation,
            current_income=current_income,
            income_goal=income_goal,
            experience_years=experience_years,
            user_skills=user_skills,
            recommended_career=recommended_career,
            income_min=expected_min,
            income_max=expected_max,
            skill_gap=skill_gap,
            location_demand=local_job_demand,
            income_goal_met=income_goal_met,
            training_cost=training_cost,
            duration_weeks=training_duration_weeks
        )

        response_data = {
            "available": True,
            "current_occupation": occupation,
            "current_income": current_income,
            "income_goal": income_goal,
            "recommended_career": recommended_career,
            "expected_income_range": {
                "min": expected_min,
                "max": expected_max
            },
            "required_skills": required_skills,
            "skill_overlap": skill_overlap,
            "skill_gap": skill_gap,
            "training_cost": training_cost,
            "training_duration": duration_text,
            "training_duration_weeks": training_duration_weeks,
            "experience_discount_applied": experience_discount_applied,
            "local_job_demand": local_job_demand,
            "estimated_roi": estimated_roi,
            "payback_period_months": payback_period_months,
            "income_goal_met": income_goal_met,
            "income_goal_note": income_goal_note,
            "available_jobs": available_jobs,
            "location": location,
            "ai_explanation": ai_explanation
        }

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error in career recommendation endpoint: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
