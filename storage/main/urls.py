from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order-details/<int:id>', views.order_detail, name='order_details'),
    path('edit-status/<int:id>', views.edit_status, name='edit_status'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('staff/', views.StaffView.as_view(), name='staff'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('edit-address/', views.edit_address, name='edit_address'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('change-qty/<str:slug>/', views.ChangeQTYView.as_view(), name='change_qty'),
    path('remove-from-cart/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
]