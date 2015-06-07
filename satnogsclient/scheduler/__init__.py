# -*- coding: utf-8 -*-
from pytz import utc

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from satnogsclient import settings

if settings.BBB_STATUS:
    import Adafruit_BBIO.GPIO as GPIO
    GPIO.setup("P8_7", GPIO.OUT)
    GPIO.output("P8_7", GPIO.LOW)
    GPIO.setup("P8_9", GPIO.OUT)
    GPIO.output("P8_9", GPIO.LOW)
    GPIO.setup("P8_11", GPIO.OUT)
    GPIO.output("P8_11", GPIO.LOW)

jobstores = {
    'default': SQLAlchemyJobStore(url=settings.SQLITE_URL)
}

executors = {
    'default': ThreadPoolExecutor(20),
}

job_defaults = {
    'coalesce': True,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
                                timezone=utc)
