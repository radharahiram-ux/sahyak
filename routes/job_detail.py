# Job detail route
import re
from urllib.parse import quote
from flask import Blueprint, render_template, session
from models import job_search_model

job_detail_bp = Blueprint('job_detail', __name__)

@job_detail_bp.route("/job/<int:job_id>")
def job_detail(job_id):
    """Display detailed view of a specific job"""
    job = job_search_model.get_job_by_id(job_id)
    if not job:
        return "Job not found", 404

    # Build a WhatsApp deep link from the listed phone number
    digits_only = re.sub(r"\D", "", job.get("phone", ""))
    whatsapp_message = f"Hi, I'm interested in the '{job.get('title', 'job')}' listing on Sahayak."
    whatsapp_link = (
        f"https://wa.me/{digits_only}?text={quote(whatsapp_message)}" if digits_only else None
    )

    saved_ids = session.get("saved_jobs", [])
    is_saved = job_id in saved_ids

    return render_template(
        "job_detail.html",
        job=job,
        whatsapp_link=whatsapp_link,
        is_saved=is_saved,
    )