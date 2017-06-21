import os
from django import forms
from .models import Trash, Task


class TrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ('name', 'location', 'remove_mode', 'dry_run')

    def clean(self):
        super(TrashForm, self).clean()
        if os.path.exists(
            os.path.join(
                self.cleaned_data['location'], self.cleaned_data['name'])
        ):
            raise forms.ValidationError(u"Path already exists.")

        return self.cleaned_data


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('trash', 'paths', 'remove_mode', 'dry_run', 'regex')


class TaskListForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status', 'trash', 'paths')

    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['countries'] = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset=Trash.objects.all(),
                                                          empty_label="Choose a countries",)
