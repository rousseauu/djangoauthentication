from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('connect/<operation>/<int:pk>/', views.change_friends, name='change_friends'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
