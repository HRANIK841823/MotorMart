from django.shortcuts import render
from car.models import Car
from brand.models import Brand
from car.models import Order
from django.contrib.auth.decorators import login_required
def home(request,brand_slug=None):
    cars=Car.objects.all()
    if brand_slug is not None:
        brand=Brand.objects.get(slug=brand_slug)
        cars=Car.objects.filter(brand=brand)
    brands=Brand.objects.all()
    return render(request,'home.html',{'cars':cars,'brands':brands})

@login_required
def profile(request):
    user_orders=Order.objects.filter(user=request.user).select_related('car')
    return render(request,'profile.html',{'orders':user_orders})