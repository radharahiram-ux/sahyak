# Main route - Home page and search functionality
from flask import Blueprint, render_template, request, session
from models import job_search_model

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """Home page with job search, category/location filters, and bookmarking"""
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    location = request.args.get("location", "").strip()

    if not search:
        jobs = job_search_model.jobs
    else:
        jobs = job_search_model.search_jobs(search)

    if category:
        jobs = [job for job in jobs if job.get("category", "").lower() == category.lower()]

    if location:
        jobs = [job for job in jobs if location.lower() in job.get("location", "").lower()]

    # Dropdown options come from the full dataset, not the filtered results
    all_categories = sorted({job.get("category", "") for job in job_search_model.jobs if job.get("category")})
    all_locations = sorted({job.get("location", "") for job in job_search_model.jobs if job.get("location")})

    saved_ids = session.get("saved_jobs", [])

    return render_template(
        "index.html",
        jobs=jobs,
        search=search,
        category=category,
        location=location,
        all_categories=all_categories,
        all_locations=all_locations,
        saved_ids=saved_ids,
    )