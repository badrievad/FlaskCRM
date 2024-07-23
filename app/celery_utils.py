import logging

from celery import Celery, Task
from flask import Flask


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def is_celery_alive(celery_app: Celery) -> bool:
    try:
        response = celery_app.control.ping(timeout=1)
        if response:
            return True
    except Exception as e:
        logging.info(f"CELERY: {e}")
        pass
    return False
