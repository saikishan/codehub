from celery import task

@task
def send_test(name):
    print("this is just a test")