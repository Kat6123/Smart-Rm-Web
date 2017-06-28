# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
import os
from django.db import models

REMOVE_MODES = (
    ('F', _('file')),
    ('D', _('directory')),
    ('R', _('recursive'))
)

TASK_STATUS = (
    ('R', _('running')),
    ('C', _('completed')),
    ('W', _('waiting'))
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
        max_length=10, choices=TASK_STATUS, default="W",
        verbose_name=_('Status')
    )
    trash = models.ForeignKey(
        Trash, on_delete=models.CASCADE, verbose_name=_('Trash'))
    remove_mode = models.CharField(
        max_length=10, choices=REMOVE_MODES, default="R",
        verbose_name=_('Remove mode')
    )
    dry_run = models.BooleanField(default=False, verbose_name=_('Dry run'))
    regex = models.CharField(
        max_length=30, blank=True, default="",
        verbose_name=_('Regex'))
    parallel_remove = models.BooleanField(
        default=False,
        verbose_name=_('Parallel remove'))
    paths = models.TextField(blank=True, verbose_name=_('Paths'))
    time = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.id)
