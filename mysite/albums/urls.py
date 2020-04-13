from django.urls import path
from . import views


app_name = 'albums'
urlpatterns = [
    path('photo/', views.upload_photo, name='upload_photo')
]