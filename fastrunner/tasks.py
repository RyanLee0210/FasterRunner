import logging
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from fastrunner import models
from fastrunner.utils.loader import save_summary, debug_suite, debug_api
from fastrunner.utils.send_email import send_email_reports
logger = logging.getLogger('FasterRunner')


@shared_task
def async_debug_api(api, project, name, config=None):
    """异步执行api
    """
    logger.info("async_debug_api start!!!")
    summary = debug_api(api, project, config=config, save=False)
    save_summary(name, summary, project)


@shared_task
def async_debug_suite(suite, project, obj, report, config):
    """异步执行suite
    """
    logger.info("async_debug_suite start!!!")
    summary = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(report, summary, project)



@shared_task
def schedule_debug_suite(*args, **kwargs):
    """定时任务
    """
    logger.info("schedule_debug_suite start!!!")
    project = kwargs["project"]
    task_name = kwargs["taskname"]
    suite = []
    test_sets = []
    config_list = []
    for pk in args:
        try:
            name = models.Case.objects.get(id=pk).name
            suite.append({
                "name": name,
                "id": pk
            })
        except ObjectDoesNotExist:
            pass

    for content in suite:
        test_list = models.CaseStep.objects. \
            filter(case__id=content["id"]).order_by("step").values("body")

        testcase_list = []
        config = None
        for content in test_list:
            body = eval(content["body"])
            if "base_url" in body["request"].keys():
                config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
                continue
            testcase_list.append(body)
        config_list.append(config)
        test_sets.append(testcase_list)

    summary = debug_suite(test_sets, project, suite, config_list, save=False)
    save_summary(task_name, summary, project, type=3)

    email_setting = kwargs
    send_email_reports(email_setting,summary)
