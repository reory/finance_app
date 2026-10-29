import logging

# This grabs the "security" configuration from base.py LOGGING dict
logger = logging.getLogger("security")


def log_suspicious_activity(message: str):
    """Logs security events like failed login attempts."""
    logger.warning(message)
