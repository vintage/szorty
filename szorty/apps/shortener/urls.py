from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.CreateShortcutView.as_view(),
        name='shortcut_create'),
    url(r'^detail,(?P<slug>[-\d\w]+)', views.DetailShortcutView.as_view(),
        name='shortcut_detail'),
    url(r'^(?P<name>\w+)', views.RedirectShortcutView.as_view(),
        name='shortcut_redirect'),
]
