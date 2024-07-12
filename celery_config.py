from celery import Celery

def make_celery(app_name=__name__):
    return Celery(app_name, broker='pyamqp://guest@localhost//', backend='rpc://')

celery = make_celery()
