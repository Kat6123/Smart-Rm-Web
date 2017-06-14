from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.trash_list, name='trash_list'),

    # url(r'^new/$', views.new_trash, name='new_trash'),

    url(r'^(?P<trash_name>[\w\d_]+)/$',
        views.trash_detail, name='trash_detail'),

    # url(r'^(.+)/settings/$', views.trash_settings, name='trash_settings'),

    url(r'^(?P<trash_name>[\w\d_]+)?/task/$',
        views.task_list, name='task_list'),

    url(r'^[\w\d_]+/task/(?P<pk>\d)+/$',
        views.task_detail, name='task_detail'),

    # url(r'^(.+)/task/(\d+)/run/$', views.run_detail, name='run_task'),
    # url(r'^(.+)/task/(\d+)/result/$', views.task_result, name='task_result'),
]
