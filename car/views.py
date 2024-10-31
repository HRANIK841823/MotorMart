from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import FormView
from django.http import  HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from .models import Car,Order
# Create your views here.
class RegisterView(FormView):
    template_name='register.html'
    form_class=forms.RegistrationFrom
    success_url=reverse_lazy('register')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Account Created Successfully')
        return HttpResponseRedirect(self.get_success_url())
class UserLoginView(LoginView):
    template_name = 'login.html'
    # success_url = reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
@login_required
def user_logout(request):
    logout(request)
    return redirect('homepage')


class DetailCarView(DetailView):
    model=Car
    pk_url_kwarg='id'
    template_name='car_details.html'
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        car= self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object # post model er object ekhane store korlam
        comments = car.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

@login_required
def buy_now(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()

        Order.objects.create(user=request.user, car=car)

        messages.success(request, f"You have successfully purchased {car.name}.")
    else:
        messages.error(request, f"Sorry, {car.name} is out of stock.")

    return redirect('car_details',id=car.id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'update_profile.html', {'form' : profile_form})