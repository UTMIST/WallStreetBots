from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def task_runner():
    """
    Dummy function for now to test the scheduling
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(dummy_function, 'interval', seconds=5)
    scheduler.start()


def dummy_function():
    print("function called")