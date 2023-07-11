from django.urls import path
from todoapp import views
urlpatterns = [
    path('dashboard',views.dashboard),
    path('register',views.user_register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),
    path('catfilter/<cv>',views.catfilter),
    path('statfilter/<sv>',views.statfilter),
    path('datesort/<dv>',views.datesort),
    path('datefilter',views.datefilter),
   



]
