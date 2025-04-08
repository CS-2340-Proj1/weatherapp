from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='favorites.index'),
    path('<int:id>/add/', views.add, name='favorites.add'),
    path('clear/', views.clear, name='favorites.clear'),
    path('purchase/', views.purchase,name='favorites.purchase'),
]