from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [


    path('register/', views.signup),
    path('register-verify/', views.verify_signup),
    
    path('login/', views.login),
    
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    path('countries/', views.countries),
    path('countries/<int:pk>/', views.country_detail),

    path('get_states/', views.states),
    path('get_states/<int:pk>/', views.state_detail),

    path('cities/', views.cities),
    path('cities/<int:pk>/', views.city_detail),


    path('user/', views.get_user),



    path('all-academies/', views.get_acadmies_filtered),
    
    path('requests/', views.get_all_requests_and_create),
    path('requests/<int:pk>/', views.request_update),



    path('get_court_types/', views.get_court_types),
    path('get_court_types/<int:pk>/', views.get_court_type),

    path('get_court_types_2/<int:court_type_id>/', views.get_court_types_2),
    path('get_court_type_2/<int:pk>/', views.get_court_type_2),




    path('courts/images/create/', views.create_court_images),
    path('courts/images/<int:image_id>/delete/', views.delete_court_images),

    path('courts/videos/create/', views.create_court_videos),
    path('courts/videos/<int:video_id>/delete/', views.delete_court_videos),
    
    path('courts/features/create/', views.create_court_features),
    path('courts/features/<int:feature_id>/delete/', views.delete_court_feature),

    path('courts/tools/create/', views.create_court_tools),
    path('courts/tools/<int:court_id>/delete/', views.delete_court_tool),

    
    path('courts/<int:court_id>/books/', views.court_books), # get court books
    path('courts/create/', views.create_court),
    path('courts/', views.get_courts),
    path('courts/<int:court_id>/', views.get_court),
    path('courts/<int:court_id>/update/', views.court_update),
    path('courts/<int:court_id>/delete/', views.court_delete),
    path('courts/all_times/', views.get_admin_times),




    path('books/check/<int:court_id>/', views.check_while_booking),


    path('books/create/', views.create_book),
    path('books/', views.get_user_books),
    path('books/<int:book_id>/', views.get_user_book),
    path('books/<int:book_id>/update/', views.book_update),

    path('books/time/<int:time_id>/', views.book_time),
    path('books/time/<int:time_id>/update/', views.book_time_update),

    path('books/over_time/create/', views.create_over_time),
    path('books/over_time/<int:over_time_id>/delete/', views.delete_over_time),



    path('settings/<int:setting_id>/numbers/', views.get_numbers),
    path('settings/<int:number_id>/numbers/delete/', views.delete_numbers),
    path('settings/numbers/create/', views.create_number),

    path('settings/', views.get_settings),
    path('settings/update/', views.update_settings),



    path('staffs/', views.get_staffs),
    path('staffs/<int:staff_id>/', views.staff_details),

    
    path('notifications/create/', views.create_notification),


    path('customers/', views.court_customer_list),
    path('customers/<int:pk>/', views.court_customer_detail),
    



    # admin
    path('users/', views.users),
    path('users/<int:pk>/', views.user_detail),

    path('types/', views.get_court_types),
    path('types/<int:pk>/', views.get_court_type),


    path('courts-admin/', views.courts),
    path('court-admin/<int:pk>/', views.court_detail),

    path('courts-type-admin/', views.court_type),
    path('courts-type-admin/<int:pk>/', views.court_type_detail),

    path('courts-type2-admin/', views.court_type_2),
    path('courts-type2-admin/<int:pk>/', views.court_type_2_detail),


    path('requests-admin/', views.requests),
    path('requests-admin/<int:pk>/', views.request_detail),

    path('features-admin/<int:court_id>/', views.court_features),
    path('features-admin/<int:pk>/', views.court_feature_detail),

    path('additional/', views.court_additionals),
    path('additional/<int:pk>/', views.court_additional_detail),

    path('additional-tool/<int:pk>/', views.court_additional_tool_detail),
    path('additional-tools/<int:additional_id>/', views.court_additional_tools),

    path('book-admin/<int:pk>/', views.book_detail),
    path('books-admin/', views.books),

    path('time-admin/<int:pk>/', views.book_time_detail),
    path('times-admin/<int:book_id>/', views.book_times),

    path('over-time-admin/<int:pk>/', views.overtime_detail),
    path('over-time-admin/<int:book_id>/', views.overtimes),

    path('setting-admin/<int:pk>/', views.setting_detail),
    path('setting-admin/<int:user_id>/', views.settings_admin),

    path('books-admin-details/', views.get_books_details_admin),
    path('courts-admin-details/', views.get_latest_courts),

 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

