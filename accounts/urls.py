from django.urls import path


from accounts import views




urlpatterns= [
path('register/',views.SignupView.as_view(),name='signup'),
path('login/',views.Loginview.as_view(),name='login'),
path('token/refresh/',views.RefreshTokenView.as_view(),name='refresh'),
path('logout/',views.LogoutView.as_view(),name='logout'),
    path("me/", views.ProfileAPIView.as_view()),
]