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
    clean_by_trash_model,
    get_trash_by_model,
    delete_trash_by_model,
    restore_by_trash_model
)
from trash_manager.trash_shortcut.remove_api import (
    parallel_remove,
    remove
)


def trash_list(request):
    trash_name_list = Trash.objects.order_by('name')
    if request.method == "POST":        # TODO: 404 obj
        trash_query = [get_object_or_404(Trash, name=trash_name)
                       for trash_name in request.POST.getlist('choices')]
        for trash in trash_query:
            delete_trash_by_model(trash)
        trash_name_list = Trash.objects.order_by('name')
        return render(request,
                      'trash_manager/trash_deleted.html',
                      {'trashs': trash_name_list}
                      )
    return render(request,
                  'trash_manager/t_trash_list.html',
                  {'trashs': trash_name_list})


def trash_content(request, trash_name):
    trash_model = get_object_or_404(Trash, name=trash_name)

    if request.method == "POST":
        if u'restore' in request.POST:
            result = restore_by_trash_model(
                trash_model, request.POST.getlist('choices')
            )
            return render(
                request, 'trash_manager/trash_info_list.html',
                {'info': result}
            )
        if u'clean' in request.POST:
            result = clean_by_trash_model(
                trash_model, request.POST.getlist('choices')
            )
            return render(
                request, 'trash_manager/trash_info_list.html',
                {'info': result}
            )
    trash = get_trash_by_model(trash_model)
    trash_content = trash.view()
    return render(request,
                  'trash_manager/t_trash_content.html',
                  {'info': trash_content, 'trash_name': trash_name}
                  )


def trash_settings(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    if request.method == "POST":
        form = TrashEditForm(request.POST, instance=trash)
        if form.is_valid():
            form.save()
            return redirect('trash_content', trash_name=trash_name)
    else:
        form = TrashEditForm(instance=trash)
    return render(request, 'trash_manager/settings.html',
                  {'action': 'Edit trash', 'form': form})


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
    return render(request, 'trash_manager/settings.html',
                  {'action': 'New trash', 'form': form})


def delete_trash(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    delete_trash_by_model(trash)

    return render(
        request, 'trash_manager/trash_deleted.html', {'name': trash_name}
    )


def task_list(request, trash_name=None):
    if request.method == "POST":        # TODO: 404 obj
        task_query = (get_object_or_404(Task, pk=pk)
                      for pk in request.POST.getlist('choices'))
        for task in task_query:
            task.delete()

    if trash_name is not None:
        trash = get_object_or_404(Trash, name=trash_name)
        task_name_list = trash.task_set.filter(
            Q(status="W") | Q(status="R")).order_by('id')
    else:
        task_name_list = Task.objects.filter(
            Q(status="W") | Q(status="R")).order_by('id')

    return render(request,
                  'trash_manager/t_task_list.html',
                  {'task_list': task_name_list}
                  )


def history(request):
    task_list = Task.objects.filter(status="C")
    if request.method == "POST":
        task_list.delete()
    return render(request,
                  'trash_manager/t_history.html',
                  {'task_list': task_list}
                  )


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        print request.POST
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if u'add_paths' in request.POST:
                form.cleaned_data['trash'] = form.cleaned_data['trash'].name
                request.session['form'] = form.cleaned_data
                params = urllib.urlencode({'path': os.path.expanduser('~')})
                return redirect(reverse('filesystem') + "?%s" % params)

            if u'stop_adding' in request.POST:
                form_data = request.session['form']
                form_data['trash'] = get_object_or_404(
                    Trash, name=form_data['trash']
                )
                form = TaskForm(initial=form_data)
                return render(request, 'trash_manager/task_edit.html',
                              {'form': form, 'action': 'Edit task'})
            form.save()
            if u'continue' in request.POST:
                return redirect('task_edit', pk=form.instance.pk)
            if u'close' in request.POST:
                return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'trash_manager/task_edit.html',
                  {'form': form, 'action': 'Edit task'})


def new_task(request, trash_name=None):     # TODO: if not None ->default trash
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            if u'continue' in request.POST:
                return redirect('new_task')
            if u'close' in request.POST:
                return redirect('task_list')
            return redirect('task_edit',        # TODO
                            pk=form.instance.id)
    else:
        form = TaskForm()
    return render(request, 'trash_manager/task_edit.html',
                  {'form': form, 'action': 'New task'})


def run_task(request, pk=0):
    task = get_object_or_404(Task, pk=pk)

    result = []

    if task.status == 'W':      # TODO add check only one task!
        task.status = "R"
        task.save()

        trash = get_trash_by_model(task.trash)
        paths = task.paths.split(' ')
        if task.parallel_remove:
            result, task.time = parallel_remove(trash, paths)
        else:
            result, task.time = remove(trash, paths)

        task.status = "C"
        task.save()

    return render(
        request, 'trash_manager/trash_info_list.html', {'info': result})


def filesystem(request):
    path = os.path.expanduser('~')
    if request.method == "GET":
        path = request.GET['path']

    if request.method == "POST":
        if u'add' in request.POST:
            path = request.POST['path']
            form_data = request.session['form']
            form_data['paths'] = "{old_paths} {new_paths}".format(
                old_paths=form_data['paths'],
                new_paths=" ".join(
                    "{root}/{name}".format(root=path, name=name)
                    for name in request.POST.getlist('choices'))
            )
            request.session.modified = True
            params = urllib.urlencode({'path': request.POST['path']})
            return redirect(reverse('filesystem') + "?%s" % params)

    root_path = ""
    directories = files = []
    for root, dirnames, filenames in os.walk(path):
        root_path = root
        directories = dirnames
        files = filenames
        break

    return render(
        request, 'trash_manager/filesystem.html',
        {'path': root_path, 'directories': directories,
         'files': files})
