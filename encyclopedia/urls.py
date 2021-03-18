from django.urls import path
from . import views


app_name = 'wikipedia'
urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<title>', views.entries, name='page-name'),
    path('new_page', views.new_page, name='create-new-page'),
    path('wiki/<title>/edit', views.edit_page, name='edit-page'),
    path('wiki/<title>/delete', views.delete_page, name='delete-page'),
    path('random', views.random_page, name='random-page'),
    path('search', views.search, name='search')
]
