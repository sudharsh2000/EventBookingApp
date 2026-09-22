from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from accounts.models import User, VendorProfile
from bookings.models import Booking
from events.models import Event


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("dashboard:login")
    def test_func(self):
        return self.request.user.is_staff


class StaffLoginView(LoginView):
    template_name = "dashboard/login.html"
    def get_success_url(self):
        return reverse_lazy("dashboard:home")


class StaffLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("dashboard:login")


class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_customers"] = User.objects.filter(role="customer").count()
        ctx["total_vendors"] = VendorProfile.objects.count()
        ctx["total_events"] = Event.objects.count()
        ctx["total_bookings"] = Booking.objects.filter(status="confirmed").count()
        return ctx


class VendorListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/vendor_list.html"
    context_object_name = "vendors"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        qs = VendorProfile.objects.select_related("user")
        return qs.filter(Q(company_name__icontains=q)) if q else qs


class EventListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/event_list.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        qs = Event.objects.select_related("vendor")
        return qs.filter(Q(title__icontains=q)) if q else qs


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    fields = ["vendor", "category", "title", "description", "venue", "city", "start_time", "end_time", "total_seats", "price", "status"]
    template_name = "dashboard/event_form.html"
    success_url = reverse_lazy("dashboard:event_list")


class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    fields = ["title", "description", "venue", "city", "start_time", "end_time", "total_seats", "price", "status"]
    template_name = "dashboard/event_form.html"
    success_url = reverse_lazy("dashboard:event_list")


class UserListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/user_list.html"
    context_object_name = "users"
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        qs = User.objects.all()
        return qs.filter(Q(email__icontains=q) | Q(referral_code__icontains=q)) if q else qs