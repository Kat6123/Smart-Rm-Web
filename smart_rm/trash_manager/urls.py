from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.trash_list, name='trash_list'),
    url(r'^task/$', views.task_list, name='task_list'),
    url(r'^history/$', views.history, name='history'),

    url(r'^lang/(?P<code>[\w-]+)/$', views.lang, name='lang'),

    url(r'^new/', include([
        url(r'^trash/$', views.new_trash, name='new_trash'),
        url(r'^task/$', views.new_task, name='new_task'),
        ])),

    url(r'^trash/(?P<trash_name>[\w\d_]+)/', include([
        url(r'^$', views.trash_content, name='trash_content'),
        url(r'^task/$', views.task_list, name='task_list'),
        url(r'^settings/$', views.trash_settings, name='trash_settings'),
        ])),


    url(r'^task/(?P<pk>\d+)/', include([
        url(r'^settings/$', views.task_settings, name='task_settings'),
        url(r'^run/$', views.run_task, name='run_task'),
        ])),

    url(r'^filesystem/$', views.filesystem, name='filesystem')
]
