# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import urllib
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Trash, Task
from .forms import TrashNewForm, TrashEditForm, TaskForm
from trash_manager.trash_shortcut.model_operations import (
    get_trash_by_model,
    delete_trash_by_model
)
from trash_manager.trash_shortcut.remove_api import (
    parallel_remove,
    remove
)


def trash_list(request):
    trash_name_list = Trash.objects.order_by('name')

    if request.method == "POST":            # Request to delete tash list
        trash_names = request.POST.getlist('choices')
        trash_query = (Trash.objects.get(name=trash) for trash in trash_names)

        for trash in trash_query:
            delete_trash_by_model(trash)

        trash_name_list = Trash.objects.order_by('name')
        return render(request,
                      'trash_manager/trash_deleted.html',
                      {'trashs': trash_name_list}
                      )

    return render(request, 'trash_manager/t_trash_list.html',
                  {'trashs': trash_name_list})


def task_list(request, trash_name=None):
    if request.method == "POST":        # Request to delete task list
        task_id_list = request.POST.getlist('choices')

        task_query = (Task.objects.get(pk=pk) for pk in task_id_list)
        for task in task_query:
            task.delete()

    if trash_name is not None:
        trash = get_object_or_404(Trash, name=trash_name)
        task_manager = trash.task_set
    else:
        task_manager = Task.objects

    task_list = task_manager.filter(
        Q(status="W") | Q(status="R")).order_by('id')

    return render(request,
                  'trash_manager/t_task_list.html',
                  {'task_list': task_list}
                  )


def history(request):
    task_list = Task.objects.filter(status="C")

    if request.method == "POST":    # Request to clean history
        task_list.delete()

    return render(request, 'trash_manager/t_history.html',
                  {'task_list': task_list}
                  )


def trash_content(request, trash_name):
    trash_model = get_object_or_404(Trash, name=trash_name)
    trash = get_trash_by_model(trash_model)

    if request.method == "POST":
        paths = request.POST.getlist('choices')
        if u'restore' in request.POST:
            result = trash.restore(os.path.basename(path)
                                   for path in paths)
            context = {'trash': trash_model,
                       'action': u'restore', 'info': result}
        elif u'clean' in request.POST:
            result = trash.remove_files_from_trash_permanently(paths)
            context = {'trash': trash_model,
                       'action': u'clean', 'info': result}
        return render(
            request, 'trash_manager/i_trash_info.html', context)

    trash_content = trash.view()
    return render(request, 'trash_manager/t_trash_content.html',
                  {'info': trash_content, 'trash_name': trash_name}
                  )


def new_trash(request):
    if request.method == "POST":
        form = TrashNewForm(request.POST)
        if form.is_valid():
            form.save()
            if u'continue' in request.POST:
                return redirect('new_trash')
            if u'close' in request.POST:
                return redirect('trash_list')
    else:
        form = TrashNewForm()
    return render(request, 'trash_manager/f_trash_settings.html',
                  {'action': 'New trash', 'form': form})


def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            print form.instance.regex
            if u'close' in request.POST:
                return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'trash_manager/f_task_settings.html',
                  {'form': form, 'action': 'New task'})


def trash_settings(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    if request.method == "POST":
        form = TrashEditForm(request.POST, instance=trash)
        if form.is_valid():
            form.save()
            if u'close' in request.POST:
                return redirect('trash_content', trash_name=trash_name)
    else:
        form = TrashEditForm(instance=trash)
    return render(request, 'trash_manager/f_trash_settings.html',
                  {'action': 'Edit trash', 'form': form})


def task_settings(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        if request.GET.get("add", "") == 'paths':
            print request.session['paths']
            form = TaskForm(instance=task,
                            initial={'paths': request.session['paths']})
    elif request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if u'close' in request.POST:
                return redirect('task_list')
            if u'add_paths' in request.POST:
                form.cleaned_data['trash'] = form.cleaned_data['trash'
                                                               ].name
                request.session['form_id'] = form.instance.id
                request.session['paths'] = form.cleaned_data['paths']
                params = urllib.urlencode(
                    {'path': os.path.expanduser('~')}
                )
                return redirect(reverse('filesystem') + "?%s" % params)
    else:
        form = TaskForm(instance=task)

    return render(request, 'trash_manager/f_task_settings.html',
                  {'form': form, 'action': 'Edit task'})


def run_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    result = []

    if task.status == 'W':      # TODO add check only one task!
        task.status = "R"
        task.save()

        trash = get_trash_by_model(task.trash)
        paths = task.paths.split(' ')
        if task.parallel_remove:
            result, task.time = parallel_remove(trash, paths, task.regex)
        else:
            result, task.time = remove(trash, paths, task.regex)

        task.status = "C"
        task.save()

    return render(
        request, 'trash_manager/i_run_task_info.html',
        {'task': task, 'info': result}
    )


def filesystem(request):
    path = os.path.expanduser('~')

    if request.method == "GET":
        path = request.GET['path']

    if request.method == "POST":
        cur_path = request.POST.get('path', path)
        request.session['paths'] = "{old_paths} {new_paths}".format(
            old_paths=request.session['paths'],
            new_paths=" ".join(
                "{root}/{name}".format(root=cur_path, name=name)
                for name in request.POST.getlist('choices'))
        )
        params = urllib.urlencode({'path': request.POST['path']})
        return redirect(reverse('filesystem') + "?%s" % params)

    root_path = ""
    directories = files = []
    for root, dirnames, filenames in os.walk(path):
        root_path = root
        directories = dirnames
        files = filenames
        break

    return render(request, 'trash_manager/t_filesystem.html',
                  {'path': root_path, 'directories': directories,
                   'files': files, 'id': request.session['form_id']})
