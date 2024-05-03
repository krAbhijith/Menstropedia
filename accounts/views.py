import datetime
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, RedirectView, ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from blogs.models import Blog, Comment, Saved
from .models import UserDetial

class AccountRegisterView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/index.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        password = self.request.POST.get('password')
        gender = self.request.POST.get('gender')
        print(gender)
        age = self.request.POST.get('age')
        form.instance.username = self.request.POST.get('email')
        form.instance.password = make_password(password)

        self.object = form.save()
        UserDetial.objects.create(age=age, gender=gender, user=self.object)
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
    

class AccountLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/index.html')

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        

class AccountLogoutView(RedirectView):
    query_string = False
    pattern_name = 'login-account'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse_lazy(self.pattern_name)
    
class ProfileView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'accounts/profile.html'
    context_object_name = 'blogs'

    login_url = 'register-account'
    redirect_field_name = 'redirected_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        comments = Comment.objects.all()
        saved_blogs = Saved.objects.filter(user = user)
        user_detial = get_object_or_404(UserDetial, user = user)
        context['comments_dict'] = comments  # Pass comments dictionary to the template
        context['saved_blogs'] = saved_blogs
        context['next_date'] = user_detial.next_men_date
        context['cycle_length'] = user_detial.cycle_length
        return context
    
class TrackerView(LoginRequiredMixin, View):

    login_url = 'register-account'
    redirect_field_name = 'redirected_to'

    def post(self, request, *args, **kwargs):
        last_men_date = request.POST.get('last_men_date')
        last_men_date = datetime.datetime.strptime(last_men_date, "%Y-%m-%d")
        period_length = request.POST.get('period_length')
        next_men_date = last_men_date + datetime.timedelta(days= int(period_length))
        user = request.user
        user_detial = get_object_or_404(UserDetial, user=user)

        user_detial.last_men_date = last_men_date
        user_detial.period_length = period_length
        user_detial.next_men_date = next_men_date + datetime.timedelta(days=user_detial.cycle_length)
        user_detial.save()

        return redirect('home')

class TrackerUpdateView(LoginRequiredMixin, View):

    login_url = 'register-account'
    redirect_field_name = 'redirected_to'


    def post(self, request, *args, **kwargs):
        tolerance = int(request.POST.get('tolerance'))
        user_detial =get_object_or_404(UserDetial, user = self.request.user)
        user_detial.cycle_length += tolerance
        user_detial.last_men_date = user_detial.next_men_date + datetime.timedelta(days=tolerance)
        user_detial.next_men_date = user_detial.last_men_date + datetime.timedelta(days=user_detial.cycle_length)
        user_detial.save()

        return redirect('home')
    
class TrackerCorrectView(LoginRequiredMixin, View):

    login_url = 'register-account'
    redirect_field_name = 'redirected_to'

    def get(self, request, *args, **kwargs):
        user_detial = get_object_or_404(UserDetial, user = self.request.user)
        user_detial.last_men_date = user_detial.next_men_date
        user_detial.next_men_date = user_detial.last_men_date + datetime.timedelta(days=user_detial.cycle_length)
        user_detial.save()

        return redirect('home')

