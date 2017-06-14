# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Trash, Task


def trash_list(request):
    trash_name_list = Trash.objects.order_by('name')[:5]
    output = ', '.join([str(t) for t in trash_name_list])
    return HttpResponse(output)


def trash_detail(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    return HttpResponse(trash)


def task_list(request, trash_name):
    trash = get_object_or_404(Trash, name=trash_name)
    task_name_list = trash.task_set.all()
    output = ', '.join([str(t) for t in task_name_list])
    return HttpResponse(output)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return HttpResponse(task)
