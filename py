root@opexwise-dev2:/opt/superset# cd docker/pythonpath_dev/
root@opexwise-dev2:/opt/superset/docker/pythonpath_dev# cat superset_config.py
import logging
import os
from datetime import timedelta
from cachelib.file import FileSystemCache
from celery.schedules import crontab
from typing import Optional

'''
---------------------------KEYCLOAK ----------------------------
'''
# Uncomment and configure the following lines for Keycloak integration
# curr = os.path.abspath(os.getcwd())
# AUTH_TYPE = AUTH_OID
# SECRET_KEY = 'opexwisesupersetintegration'
# OIDC_CLIENT_SECRETS = curr + '/pythonpath/client_secret.json'
# OIDC_ID_TOKEN_COOKIE_SECURE = False
# OIDC_REQUIRE_VERIFIED_EMAIL = False
# OIDC_OPENID_REALM = 'opexwise'
# OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
# CUSTOM_SECURITY_MANAGER = OIDCSecurityManager
# AUTH_USER_REGISTRATION = False
# AUTH_USER_REGISTRATION_ROLE = 'Alpha'
'''
--------------------------------------------------------------
'''

ENABLE_CORS = True
# ENABLE_PROXY_FIX = True
 #PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 0, "x_prefix": 1}

PREFERRED_URL_SCHEME = 'https'
SUPERSET_WEBSERVER_PROTOCOL = "https"

HTTP_HEADERS = {}

PUBLIC_ROLE_LIKE = "Gamma"

SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

WTF_CSRF_ENABLED = False

# Alert 
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

# Migration to PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql://superset:superset@10.10.50.23:8005/superset"

FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_TEMPLATE_PROCESSING": True
}
TEMPLATES_EXTENSIONS = ['superset_jinja2_ext']
LOGIN_REDIRECT_URL = '/login'
DISABLED_TOP_LEVEL_NAV_ITEMS = ['Dashboards', 'Charts', 'Data', 'Settings', 'Datasets']
# STATIC_FILES_EXCLUDE_LIST = ['static/assets/package.json']

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(var_name)
            raise EnvironmentError(error_msg)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks")
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
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

# Email configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_STARTTLS = True
SMTP_SSL_SERVER_AUTH = True
SMTP_SSL = False
SMTP_USER = "iopexdashboard@gmail.com"
SMTP_PASSWORD = "vxcjhrfvuylgwfcb"
SMTP_MAIL_FROM = "iopexdashboard@gmail.com"
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] "
SQLLAB_CTAS_NO_LIMIT = True

# WebDriver configuration
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]
WEBDRIVER_BASEURL = "https://dev.opexwise.ai:8003"


ENABLE_PROXY_FIX = True
PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 0, "x_prefix": 1}
