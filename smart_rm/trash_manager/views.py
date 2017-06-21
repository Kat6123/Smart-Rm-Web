# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Trash, Task
from .forms import TrashForm, TaskForm
from .set_trash import (
    get_trash_by_model,
    delete_trash_by_model,
    restore_by_trash_model,
    parallel_remove
)


def ex(request):
    return HttpResponse(request.GET)


def trash_list(request):
    trash_name_list = Trash.objects.order_by('name')
    return render(request,
                  'trash_manager/trash_list.html', {'trashs': trash_name_list})


def trash_content(request, trash_name):
    trash_model = get_object_or_404(Trash, name=trash_name)

    if request.method == "POST":
        print request.POST['choices']
        if u'restore' in request.POST:
            result = restore_by_trash_model(
                trash_model, request.POST['choices']
            )
            return render(
                request, 'trash_manager/trash_info_list.html',
                {'info': result}
            )
        if u'close' in request.POST:
            return redirect('trash_list')

    trash = get_trash_by_model(trash_model)
    trash_content = trash.view()
    return render(request,
                  'trash_manager/trash_content.html',
                  {'info': trash_content, 'trash_name': trash_name}
                  )


def trash_settings(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    if request.method == "POST":
        form = TrashForm(request.POST, instance=trash)
        if form.is_valid():
            form.save()
            return redirect('trash_content', name=trash_name)
    else:
        form = TrashForm(instance=trash)
    return render(request, 'trash_manager/trash_settings.html',
                  {'action': 'Edit trash', 'form': form})


def new_trash(request):
    if request.method == "POST":
        form = TrashForm(request.POST)
        if form.is_valid():
            form.save()
            if u'continue' in request.POST:
                return redirect('new_trash')
            if u'close' in request.POST:
                return redirect('trash_list')
    else:
        form = TrashForm()
    return render(request, 'trash_manager/trash_settings.html',
                  {'action': 'Create trash', 'form': form})


def clean_trash(request, trash_name):
    return HttpResponse("cleaned")


def delete_trash(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    delete_trash_by_model(trash)

    return render(
        request, 'trash_manager/trash_deleted.html', {'name': trash_name}
    )


def restore_from_trash(request, trash_name):
    return HttpResponse("restored")


def task_list(request, trash_name=None):
    if trash_name is not None:
        trash = get_object_or_404(Trash, name=trash_name)
        task_name_list = trash.task_set.all()
    else:
        task_name_list = Task.objects.order_by('id')

    return render(request,
                  'trash_manager/task_list.html',
                  {'task_list': task_name_list}
                  )


def history(request):
    task_list = Task.objects.filter(status="C")
    return render(request,
                  'trash_manager/task_list.html',
                  {'task_list': task_list}
                  )


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=pk)
    else:
        form = TaskForm(instance=task)
        print form
    return render(request, 'trash_manager/task_edit.html', {'form': form})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'trash_manager/task_detail.html', {'task': task})


def new_task(request, trash_name=None):     # TODO: if not None ->default trash
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_detail',
                            pk=form.instance.id)
    else:
        form = TaskForm()
    return render(request, 'trash_manager/task_edit.html', {'form': form})


def run_task(request, pk=0):
    task = get_object_or_404(Task, pk=pk)

    result = []

    if task.status == 'W':      # TODO add check only one task!
        task.status = "R"
        task.save()

        trash = get_trash_by_model(task.trash)
        paths = task.paths.split(' ')
        # result = trash.remove(paths)
        result = parallel_remove(trash, paths)
        task.status = "C"
        task.save()

    return render(
        request, 'trash_manager/trash_info_list.html', {'info': result})


def delete_task(request, pk=0):
    return HttpResponse("deleted {0}".format(pk))
