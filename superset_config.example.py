# import logging
import os

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

# logger = logging.getLogger()

# SUPERSET_PORT = os.getenv("SUPERSET_PORT", "8088")
ENABLE_PROXY_FIX = os.getenv("ENABLE_PROXY_FIX")

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

# EXAMPLES_USER = os.getenv("EXAMPLES_USER")
# EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
# EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
# EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
# EXAMPLES_DB = os.getenv("EXAMPLES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

# SQLALCHEMY_EXAMPLES_URI = (
#     f"{DATABASE_DIALECT}://"
#     f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
#     f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
# )

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab",)
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }

CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

WEBDRIVER_BASEURL = f"http://superset:8088/"
# The base URL for the email report hyperlinks.
# WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

# Flag that controls if limit should be enforced on the CTA (create table as queries).
# SQLLAB_CTAS_NO_LIMIT = True

# smtp server configuration
EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", False)
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", True)
SMTP_SSL = os.getenv("SMTP_SSL", False)
SMTP_USER = os.getenv("SMTP_USER", "superset")
SMTP_PORT = os.getenv("SMTP_PORT", 25)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "superset")
SMTP_MAIL_FROM = os.getenv("SMTP_MAIL_FROM", "superset@superset.com")
# EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] " # optional - overwrites default value in config.py of "[Report] "
