# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Trash, Task
from .forms import TrashForm


def trash_list(request):
    trash_name_list = Trash.objects.order_by('name')
    return render(request,
                  'trash_manager/trash_list.html', {'trashs': trash_name_list})


def trash_detail(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    return render(request,
                  'trash_manager/trash_detail.html', {'trash': trash})


def trash_settings(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    if request.method == "POST":
        form = TrashForm(request.POST, instance=trash)
        if form.is_valid():
            form.save()
            return redirect('trash_detail', name=trash_name)
    else:
        form = TrashForm(instance=trash)
    return render(request, 'trash_manager/trash_settings.html', {'form': form})


def new_trash(request):
    if request.method == "POST":
        form = TrashForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trash_detail',
                            trash_name=form.cleaned_data['name'])
    else:
        form = TrashForm()
    return render(request, 'trash_manager/trash_settings.html', {'form': form})


def task_list(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    task_name_list = trash.task_set.all()
    output = ', '.join([str(t) for t in task_name_list])
    return HttpResponse(output)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return HttpResponse(task)
