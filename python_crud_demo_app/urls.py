from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration_process', views.registration_process),
    path('login_process', views.login_process),
    path('dashboard', views.dashboard),
    path('new_vacation', views.new_vacation),
    path('vacation_process', views.vacation_process),
    path('edit_trip_process/<int:id>', views.edit_trip_process),
    path('edit_trip/<int:id>', views.edit_trip),
    path('delete/<int:id>', views.delete),
    path('view_trip/<int:id>', views.view_trip),

    path('logout', views.logout),
]