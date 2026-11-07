from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.recipe_list, name='list'),
    path('search/', views.search, name='search'),
    path('random/', views.random_recipe, name='random'),
    path('stats/', views.stats, name='stats'),
    path('category/<str:category_name>/', views.category_detail, name='category'),
    path('<int:pk>/', views.recipe_detail, name='detail'),
    path('<slug:slug>/', views.recipe_by_slug, name='recipe_by_slug'),
]