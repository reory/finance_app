import logging

# This grabs the "pipeline" configuration from the base.py LOGGING dict
logger = logging.getLogger("pipeline")


def log_pipeline_step(message: str):
    """Logs standard pipeline events like logins and registrations."""
    logger.info(message)
