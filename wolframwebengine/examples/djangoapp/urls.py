from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.urls import path

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl
from wolframwebengine.web import django_wl_view

session = WolframLanguageSession()


def django_view(request):
    return HttpResponse("hello from django")


@django_wl_view(session)
def form_view(request):
    return wl.FormFunction({"x": "String"}, wl.Identity, "JSON")


@django_wl_view(session)
def api_view(request):
    return wl.APIFunction({"x": "String"}, wl.Identity, "JSON")


urlpatterns = [
    path("", django_view, name="home"),
    path("form", form_view, name="form"),
    path("api", api_view, name="api"),
]
