from django.urls import path
from  .import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('athletes/', views.AthleteListView.as_view(), name='user-list'),
    path('athletes/<int:id>/', views.AthleteDetailView.as_view(), name='user-list'),
    path('users/<int:id>/', views.UserDetailView.as_view(), name='user-list'),
    path('sponsors/', views.SponsorListView.as_view(), name='user-list'),
    path('sponsors/<int:id>/', views.SponsorDetailView.as_view(), name='user-list'),
    path('donations/', views.DonationListView.as_view(), name='donation-list'),
    path('donations/<int:id>/', views.DonationDetailView.as_view(), name='donation-detail'),

    path('comments/', views.get_comments, name='get_comments'),
    path('comments/create/', views.create_comment, name='create_comment'),
    path('comments/update/<int:pk>/', views.update_comment, name='update_comment'),
    path('comments/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    

    path('contact/', views.ContactMessageCreateView.as_view(), name='contact_create'),
    path('contact/list/', views.ContactMessageListView.as_view(), name='contact_list'),

    # path('upload_video/', views.upload_video, name='upload_video'),
    # path('videos/', views.get_all_videos, name='get_all_videos'),
    # path('videos/<int:pk>/', views.video_detail, name='video_detail'),
 
]