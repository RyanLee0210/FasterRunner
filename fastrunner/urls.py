"""FasterRunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from fastrunner.views import project, api, config, schedule, run, suite, report

router = DefaultRouter()
# 驱动代码
router.register(r'pycode', project.PycodeView, base_name='pycode')
router.register(r'runpycode', project.PycodeRunView, base_name="runpycode")


urlpatterns = [
    url(r'^', include(router.urls)),
    # 项目相关接口地址
    path('project/', project.ProjectView.as_view({
        "get": "list",
        "post": "add",
        "patch": "update",
        "delete": "delete"
    })),
    path('project/<int:pk>/', project.ProjectView.as_view({"get": "single"})),

    # 定时任务相关接口
    path('schedule/', schedule.ScheduleView.as_view({
        "get": "list",
        "post": "add",
    })),

    path('schedule/<int:pk>/', schedule.ScheduleView.as_view({
        "delete": "delete"
    })),



    # debugtalk.py相关接口地址
    path('debugtalk/<int:pk>/', project.DebugTalkView.as_view({"get": "debugtalk"})),
    path('debugtalk/', project.DebugTalkView.as_view({
        "patch": "update",
        "post": "run"
    })),

    # 二叉树接口地址
    path('tree/<int:pk>/', project.TreeView.as_view()),

    # 文件上传 修改 删除接口地址
    # path('file/', project.FileView.as_view()),

    # api接口模板地址
    path('api/', api.APITemplateView.as_view({
        "post": "add",
        "get": "list"
    })),

    path('api/<int:pk>/', api.APITemplateView.as_view({
        "delete": "delete",
        "get": "single",
        "patch": "update",
        "post": "copy"
    })),

    # test接口地址
    path('test/', suite.TestCaseView.as_view({
        "get": "get",
        "post": "post",
        "delete": "delete"
    })),

    path('test/<int:pk>/', suite.TestCaseView.as_view({
        "delete": "delete",
        "post": "copy"
    })),

    path('teststep/<int:pk>/', suite.CaseStepView.as_view()),

    # config接口地址
    path('config/', config.ConfigView.as_view({
        "post": "add",
        "get": "list",
        "delete": "delete"
    })),

    path('config/<int:pk>/', config.ConfigView.as_view({
        "post": "copy",
        "delete": "delete",
        "patch": "update",
        "get": "all"
    })),

    path('variables/', config.VariablesView.as_view({
        "post": "add",
        "get": "list",
        "delete": "delete"
    })),

    path('variables/<int:pk>/', config.VariablesView.as_view({
        "delete": "delete",
        "patch": "update"
    })),

    # run api
    path('run_api_pk/<int:pk>/', run.run_api_pk),
    path('run_api_tree/', run.run_api_tree),
    path('run_api/', run.run_api),

    # run testsuite
    path('run_testsuite/', run.run_testsuite),
    path('run_test/', run.run_test),
    path('run_testsuite_pk/<int:pk>/', run.run_testsuite_pk),
    path('run_suite_tree/', run.run_suite_tree),
    path('automation_test/', run.automation_test),

    # 报告地址
    path('reports/', report.ReportView.as_view({
        "get": "list"
    })),

    path('reports/<int:pk>/', report.ReportView.as_view({
        "delete": "delete",
        "get": "look"
    })),

    path('host_ip/', config.HostIPView.as_view({
        "post": "add",
        "get": "list"
    })),

    path('host_ip/<int:pk>/', config.HostIPView.as_view({
        "delete": "delete",
        "patch": "update",
        "get": "all"
    })),
]
