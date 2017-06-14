# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

REMOVE_MODES = (
    ('F', 'file'),
    ('D', 'directory'),
    ('R', 'recursive')
)

TASK_STATUS = (
    ('C', 'completed'),
    ('W', 'waiting')
)


class Trash(models.Model):
    name = models.CharField(max_length=30, unique=True)
    location = models.FilePathField(path='/', default="/")
    remove_mode = models.CharField(
        max_length=1, choices=REMOVE_MODES, default="F"
    )
    dry_run = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    status = models.CharField(
        max_length=1, choices=TASK_STATUS, default="W"
    )
    trash = models.ForeignKey(Trash, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Info(models.Model):
    path = models.CharField(max_length=100)
    path_in_trash = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.path
