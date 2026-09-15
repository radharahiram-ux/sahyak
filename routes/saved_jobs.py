# Saved / bookmarked jobs feature (session-based, no login required)
from flask import Blueprint, render_template, redirect, url_for, session, request
from models import job_search_model

saved_bp = Blueprint('saved', __name__)

def _get_saved_ids():
    return session.get('saved_jobs', [])

@saved_bp.route('/saved')
def saved_jobs():
    """Show all jobs the visitor has bookmarked in this browser session"""
    saved_ids = _get_saved_ids()
    jobs = [job_search_model.get_job_by_id(job_id) for job_id in saved_ids]
    jobs = [job for job in jobs if job]  # drop any that were deleted since saving
    return render_template('saved_jobs.html', jobs=jobs)

@saved_bp.route('/save/<int:job_id>', methods=['POST'])
def toggle_save(job_id):
    """Add or remove a job from the session's saved list, then return to where the user was"""
    saved_ids = _get_saved_ids()

    if job_id in saved_ids:
        saved_ids.remove(job_id)
    else:
        saved_ids.append(job_id)

    session['saved_jobs'] = saved_ids
    session.modified = True

    next_url = request.form.get('next') or url_for('main.home')
    return redirect(next_url)