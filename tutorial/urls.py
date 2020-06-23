from django.urls import path
from  . import views

app_name = "tutorial"

urlpatterns = [
    # /
    path('', views.index, name='index'),
]
