import os
from django import forms
from .models import Trash, Task


class TrashNewForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ('name', 'location', 'remove_mode', 'dry_run')

    def clean(self):
        super(TrashNewForm, self).clean()
        if os.path.exists(
            os.path.join(
                self.cleaned_data['location'], self.cleaned_data['name'])
        ):
            raise forms.ValidationError(u"Path already exists.")

        return self.cleaned_data


class TrashEditForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ('remove_mode', 'dry_run')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('trash', 'paths', 'remove_mode',
                  'parallel_remove', 'dry_run', 'regex')
