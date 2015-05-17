from django.views.generic import edit as edit_views
from django.views.generic import detail as detail_views
from django import http

from . import models
from . import forms


class CreateShortcutView(edit_views.CreateView):
    model = models.Shortcut
    form_class = forms.ShortcutCreateForm


class DetailShortcutView(detail_views.DetailView):
    model = models.Shortcut


class RedirectShortcutView(detail_views.DetailView):
    model = models.Word
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get(self, *args, **kwargs):
        super(RedirectShortcutView, self).get(*args, **kwargs)

        shortcut = self.object.shortcut
        shortcut.visited()
        shortcut.save()

        redirect_url = shortcut.target_url
        return http.HttpResponseRedirect(redirect_url)

    def get_queryset(self):
        qs = super(RedirectShortcutView, self).get_queryset()
        return qs.filter(shortcut__isnull=False).select_related('shortcut')