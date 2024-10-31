from django.urls import path,include
from .import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('details/<int:id>',views.DetailCarView.as_view(),name='car_details'),
    path('buy/<int:car_id>',views.buy_now,name='buy_now'),
    path('prodile/edit',views.edit_profile,name='edit_profile'),
]

