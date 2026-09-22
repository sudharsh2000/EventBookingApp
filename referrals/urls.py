from django.urls import path
from referrals import views

urlpatterns = [
    path("<int:user_id>/tree/", views.ReferralTreeAPIView.as_view()),
    path("<int:user_id>/root/", views.ReferralRootAPIView.as_view()),
    path("<int:user_id>/stats/", views.ReferralStatsAPIView.as_view()),
]
