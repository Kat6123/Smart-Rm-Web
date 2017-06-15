from django import forms
from .models import Trash, Task, Info


class TrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ('name', 'location', 'remove_mode', 'dry_run')


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ('pk', 'status', 'trash')
