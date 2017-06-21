from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.trash_list, name='trash_list'),

    url(r'^history/$', views.history, name='history'),

    url(r'^new/$', views.new_trash, name='new_trash'),

    url(r'^task/$', views.task_list, name='task_list'),
    url(r'^task/new/$', views.new_task, name='new_task'),

    url(r'^(?P<trash_name>[\w\d_]+)/', include([
        url(r'^$', views.trash_content, name='trash_content'),
        url(r'^settings/$', views.trash_settings, name='trash_settings'),
        url(r'^task/$', views.task_list, name='task_list'),
        url(r'^task/new/$', views.new_task, name='new_task'),
        url(r'^delete/$', views.delete_trash, name='delete_trash'),
        ])),

    url(r'^[\w\d_]+/task/(?P<pk>\d+)/', include([
        url(r'^$', views.task_edit, name='task_edit'),
        url(r'^run/$', views.run_task, name='run_task'),
        # url(r'^delete/$', views.delete_task, name='delete_task'),
        ])),

    url(r'^[\w\d_]+/task/d+/run/$', views.run_task, name='run_task'),

    # url(r'^(.+)/task/(\d+)/result/$', views.task_result, name='task_result'),
]
