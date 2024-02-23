from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('register/', views.signup),
    path('login/', views.login),

    path('get_states/', views.get_states),
    path('states/create/', views.create_state),
    path('states/<int:state_id>/delete/', views.delete_state),
    path('states/<int:state_id>/update/', views.update_state),


    path('user/', views.get_user),


    path('get_court_types/', views.get_court_types),
    path('court_type/create/', views.create_type),
    path('court_type/<int:type_id>/delete/', views.delete_type),
    path('court_type/<int:type_id>/update/', views.update_type),


    path('courts/create/', views.create_court),
    path('courts/', views.get_courts),
    path('courts/<int:court_id>/', views.get_court),
    path('courts/<int:court_id>/update/', views.court_update),


    path('books/check/<int:court_id>/', views.check_while_booking),

    path('books/create/', views.create_book),
    path('books/', views.get_user_books),
    path('books/<int:book_id>/', views.get_user_book),
    path('books/<int:book_id>/update/', views.book_update),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

