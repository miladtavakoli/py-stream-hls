from celery import Celery

import settings

celery_app = Celery('flask-celery-app',
                    broker_url=settings.CELERY_BROKER_URL,
                    result_backend=settings.CELERY_RESULT_BACKEND,
                    broker_connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
                    broker_connection_retry=settings.BROKER_CONNECTION_RETRY,
                    broker_connection_retry_on_startup=settings.BROKER_CONNECTION_RETRY_ON_STARTUP,
                    broker_connection_max_retries=settings.BROKER_CONNECTION_MAX_RETRIES,
                    include=['celery_task.tasks']
                    )

# if __name__ == '__main__':
#     celery_app.start()
