from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('register/', views.signup),
    path('login/', views.login),

    path('get_user/', views.get_user),


    path('get_states/', views.get_states),


    path('get_courts/', views.get_courts),
    path('get_court/<int:pk>/', views.get_court),


    path('court/tools/<int:court_id>/', views.get_court_additional_tools),
    # admin
    path('court/create/', views.create_court),
    path('court/<int:court_id>/update/', views.update_court),


    path('book/create/', views.create_book),
    path('book/check/<int:court_id>/', views.check_book),
    path('books/<int:user_id>/', views.get_user_books),
    # admin
    path('books/', views.get_books),

    path('book/settings/<int:book_id>/', views.get_book_setting),
    path('book/all_settings/<int:court_id>/', views.get_book_settings), # for booking the court get all settings
    path('book/settings/<int:book_id>/update/', views.edit_book_settings),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

