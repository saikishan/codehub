from celery import task
from .models import Question,College,Result
import arrow
from scraper import Scrapie
from cache_memoize import cache_memoize
from celery.schedules import crontab
from codehub.celery import app
@cache_memoize(20*60)
@task
def scrape_question(question_id, skip_scrapped = False):
    def get_platform_names(question_url):
        if question_url.startswith("https://www.hackerrank.com/"):
            return ('results__user__hackerrank_id',"hackerrank_college_id", "user__hackerrank_id__in")

    question =  Question.objects.get(id = question_id)
    last_try = arrow.get(question.last_scraped)
    if skip_scrapped and last_try > (arrow.utcnow().shift(days=-1)):
        return
    users_key, colleges_key, result_key = get_platform_names(question.url)
    users = [user_id[0] for user_id in Question.objects.filter(id = question_id,results__status= False).values_list(users_key)]
    colleges = [college_id[0] for college_id in College.objects.filter().values_list(colleges_key)]
    print(users, colleges, question.url)
    scrape_root = Scrapie(question.url, users, colleges, question.last_scraped)
    passed_students = scrape_root.get_passed_students()
    print("got results", passed_students)
    update_query = {
        "question":question,
        result_key:passed_students
    }
    Result.objects.filter(**update_query).update(status =True)

@cache_memoize(12*60*60)
@task
def all_question_scheduler():
    for question in Question.objects.all():
        scrape_question.delay(question.id)
    return "All questions Queued"




@app.on_after_configure.connect
def setup_perodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=1), all_question_scheduler.s())
