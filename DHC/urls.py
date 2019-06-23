from django.urls import path

from . import views

urlpatterns = [
    path("", views.aiinit, name="aiinit"),
    path("update", views.update, name="update"),
    path("auto", views.auto, name="auto"),
    path("clear", views.clear, name="clear"),
    path("updateboard", views.updateboard, name="updateboard"),
    path("pvp", views.pvpinit, name="pvp"),
    path("pvpupdate", views.pvpupdate, name="pvpupdate"),
]

