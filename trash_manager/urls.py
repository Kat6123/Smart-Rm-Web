from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.trash_list, name='trash_list'),

    url(r'^new/$', views.new_trash, name='new_trash'),
    url(r'^new/create/$', views.create_new_trash, name='create_new_trash'),

    url(r'^.+/$', views.trash_detail, name='trash_detail'),

    # url(r'^(.+)/settings/$', views.trash_settings, name='trash_settings'),
    # url(r'^(.+)/settings/save/$', views.save_trash_settings, name='save_trash_settings'),
    #
    # url(r'^(.+)/task/$', views.task_list, name='task_list'),
    #
    url(r'^.+/task/[0-9]+/$', views.task_detail, name='task_detail'),
    # url(r'^(.+)/task/(\d+)/edit/$', views.edit_task, name='edit_task'),
    #
    # url(r'^(.+)/task/(\d+)/run/$', views.run_detail, name='run_task'),
    # url(r'^(.+)/task/(\d+)/result/$', views.task_result, name='task_result'),
]
