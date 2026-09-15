# Dashboard route - job market overview and stats
from collections import Counter
from flask import Blueprint, render_template
from models import job_search_model

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Show an overview of job market stats"""
    jobs = job_search_model.jobs

    total_jobs = len(jobs)

    category_counts = Counter(job.get('category', 'other') for job in jobs)
    location_counts = Counter(job.get('location', 'Unknown') for job in jobs)
    employer_counts = Counter(job.get('employer', 'Unknown') for job in jobs)

    top_categories = category_counts.most_common(8)
    top_locations = location_counts.most_common(8)

    max_category_count = max((count for _, count in top_categories), default=1)
    max_location_count = max((count for _, count in top_locations), default=1)

    # Recent jobs (assumes higher id == more recently added, matching add_job's logic)
    recent_jobs = sorted(jobs, key=lambda j: j.get('id', 0), reverse=True)[:5]

    return render_template(
        'dashboard.html',
        total_jobs=total_jobs,
        total_employers=len(employer_counts),
        total_categories=len(category_counts),
        top_categories=top_categories,
        top_locations=top_locations,
        max_category_count=max_category_count,
        max_location_count=max_location_count,
        recent_jobs=recent_jobs,
    )