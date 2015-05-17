import re
import string

from django import forms
from django.forms import models as model_forms

from . import models

WORD_DELIMITER = string.punctuation


class ShortcutCreateForm(model_forms.ModelForm):
    class Meta:
        model = models.Shortcut
        fields = ['target_url']
        widgets = {
            'target_url': forms.TextInput(attrs={
                'placeholder': 'Enter your URL'
            }),
        }

    def clean_target_url(self):
        if not models.Word.objects.exists():
            raise forms.ValidationError(
                'URL shortening is currently unavailable. The word table '
                'need to be initialized first.')

        return self.cleaned_data['target_url']

    @staticmethod
    def get_words(value):
        return re.split(r'[{}]+'.format(WORD_DELIMITER), value)

    def save(self, commit=True):
        target_url = self.data['target_url']
        words = [w.lower() for w in self.get_words(target_url)]

        free_words = models.Word.objects.filter(shortcut__isnull=True)

        if not free_words.exists():
            oldest = models.Shortcut.objects.earliest('updated_at')
            word_id = oldest.word_id
            oldest.delete()
        else:
            word_objects = dict(
                free_words.filter(name__in=words).values_list('name', 'id')
            )

            if not word_objects:
                word_id = free_words.order_by('?')[0].id
            else:
                for word in words:
                    if word in word_objects:
                        word_id = word_objects[word]
                        break

        self.instance.word_id = word_id

        return super(ShortcutCreateForm, self).save(commit=commit)