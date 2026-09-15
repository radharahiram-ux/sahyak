# Blueprint initialization file
from .main import main
from .job_detail import job_detail_bp
from .make_jobs import make_jobs_bp
from .profile import profile_bp
from .audio import audio_bp
from .career_recommendation import career_bp
from .saved_jobs import saved_bp
from .dashboard import dashboard_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(main)
    app.register_blueprint(job_detail_bp)
    app.register_blueprint(make_jobs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(saved_bp)
    app.register_blueprint(dashboard_bp)