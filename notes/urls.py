# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('notes/create/', views.create_note),
    path('notes/<int:id>/', views.get_note),
    path('notes/share/', views.share_note),
    path('notes/<int:id>/update/', views.update_note),
    path('notes/version-history/<int:id>/', views.get_note_version_history),
]
