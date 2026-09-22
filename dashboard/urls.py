from django.urls import path
from dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("login/", views.StaffLoginView.as_view(), name="login"),
    path("logout/", views.StaffLogoutView.as_view(), name="logout"),
    path("", views.DashboardHomeView.as_view(), name="home"),
    path("vendors/", views.VendorListView.as_view(), name="vendor_list"),
    path("events/", views.EventListView.as_view(), name="event_list"),
    path("events/add/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_update"),
    path("users/", views.UserListView.as_view(), name="user_list"),
]