# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
import os
from django.db import models

REMOVE_MODES = (
    ('F', 'file'),
    ('D', 'directory'),
    ('R', 'recursive')
)

TASK_STATUS = (
    ('R', 'running'),
    ('C', 'completed'),
    ('W', 'waiting')
)


class Trash(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('Name'))
    location = models.CharField(
        max_length=30,
        default=os.path.expanduser("~/.local/share/"),
        verbose_name=_('Location')
    )
    remove_mode = models.CharField(
        max_length=10, choices=REMOVE_MODES, default="R",
        verbose_name=_('Remove mode')
    )
    dry_run = models.BooleanField(default=False, verbose_name=_('Dry run'))

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Task(models.Model):
    status = models.CharField(
        max_length=10, choices=TASK_STATUS, default="W"
    )
    trash = models.ForeignKey(Trash, on_delete=models.CASCADE)
    remove_mode = models.CharField(
        max_length=10, choices=REMOVE_MODES, default="R"
    )
    dry_run = models.BooleanField(default=False)
    regex = models.CharField(max_length=30, blank=True, default="")
    parallel_remove = models.BooleanField(default=False)
    paths = models.TextField(blank=True)
    time = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.id)
