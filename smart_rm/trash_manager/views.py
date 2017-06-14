# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def trash_list(request):
    return HttpResponse("trash_list")


def new_trash(request):
    return HttpResponse("new_trash")


def create_new_trash(request):
    return HttpResponse("create_new_trash")


def trash_detail(request):
    return HttpResponse("trash_detail")


def task_detail(request):
    return HttpResponse("task_detail")
