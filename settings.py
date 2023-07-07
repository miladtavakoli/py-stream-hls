from utils.helper import join_path

# DIRECTORIES
PROJECT_DIRECTORY = '/home/noob/project/py_streaming'
MEDIA_DIRECTORY = 'media'
MEDIA_VIDEO_DIRECTORY = join_path(MEDIA_DIRECTORY, 'videos')
MEDIA_DIRECTORY_FULL_PATH = join_path(PROJECT_DIRECTORY, MEDIA_DIRECTORY)

# CELERY CONFIG
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
BROKER_CONNECTION_TIMEOUT = 10
BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = 3
BROKER_CONNECTION_RETRY_ON_STARTUP = True

# REDIS CONFIG
REDIS_URL = "localhost"
REDIS_PORT = 6379

AUTHORIZATION_EXPIRE_TIME = 60 * 60 * 24 * 30  # second
