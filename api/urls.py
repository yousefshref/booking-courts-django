from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [


    path('register/', views.signup),
    path('login/', views.login),

    path('get_states/', views.get_states),


    path('user/', views.get_user),


    path('get_court_types/', views.get_court_types),
    path('get_court_types_2/', views.get_court_types_2),




    path('courts/images/create/', views.create_court_images),
    path('courts/images/<int:image_id>/delete/', views.delete_court_images),

    path('courts/videos/create/', views.create_court_videos),
    path('courts/videos/<int:video_id>/delete/', views.delete_court_videos),
    
    path('courts/features/create/', views.create_court_features),
    path('courts/features/<int:feature_id>/delete/', views.delete_court_feature),

    path('courts/create/', views.create_court),
    path('courts/', views.get_courts),
    path('courts/<int:court_id>/', views.get_court),
    path('courts/<int:court_id>/update/', views.court_update),
    path('courts/<int:court_id>/delete/', views.court_delete),




    path('books/check/<int:court_id>/', views.check_while_booking),


    path('books/create/', views.create_book),
    path('books/', views.get_user_books),
    path('books/<int:book_id>/', views.get_user_book),
    path('books/<int:book_id>/update/', views.book_update),
    path('books/<int:book_id>/delete/', views.book_delete),

    path('books/time/<int:time_id>/', views.book_time),
    path('books/time/<int:time_id>/update/', views.book_time_update),


    path('settings/<int:setting_id>/numbers/', views.get_numbers),
    path('settings/<int:number_id>/numbers/delete/', views.delete_numbers),
    path('settings/numbers/create/', views.create_number),

    path('settings/', views.get_settings),
    path('settings/update/', views.update_settings),


    path('staffs/', views.get_staffs),
    path('staffs/<int:staff_id>/', views.staff_details),

    
    path('notifications/create/', views.create_notification),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

