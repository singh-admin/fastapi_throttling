from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

# Store failed login attempts
failed_attempts = {}

# .env settings
throttle_limit = os.getenv("MAX_ATTEMPTS")
block_duration = os.getenv("BLOCK_DURATION")


# ----------------------------  Throttling handing ----------------------------------------------------------
def log_failed_attempt(email: str):
    """Log a failed login attempt."""
    now = datetime.utcnow()
    if email in failed_attempts:
        failed_attempts[email]['attempts'] += 1
        failed_attempts[email]['last_attempt'] = now
    else:
        failed_attempts[email] = {'attempts': 1, 'last_attempt': now}


def is_throttled(email: str) -> bool:
    """Check if the user is throttled."""
    if email not in failed_attempts:
        return False

    attempts = failed_attempts[email]['attempts']
    last_attempt = failed_attempts[email]['last_attempt']

    if attempts >= int(throttle_limit):
        block_duration_timedelta = timedelta(seconds=int(block_duration))
        if datetime.utcnow() - last_attempt <= block_duration_timedelta:
            return True  # Throttled
        else:
            reset_attempts(email)  # Reset after block duration

    return False


def reset_attempts(email: str):
    """Reset failed attempts for a user."""
    if email in failed_attempts:
        del failed_attempts[email]
