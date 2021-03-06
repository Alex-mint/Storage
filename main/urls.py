from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cart/', views.CartVueView.as_view(), name='cart'),
    path('cart-vue/', views.CartVueView.as_view(), name='cart-vue'),
    path('about-us/', views.AboutUs.as_view(), name='about_us'),
    path('contact-us/', views.ContactUs.as_view(), name='contact_us'),
    path('success/', views.Success.as_view(), name='success'),
    path('pay-order/', views.StripeView.as_view(), name='pay_order'),
    path('order-details/<int:id>', views.order_detail, name='order_details'),
    path('order-view/<int:id>', views.order_view, name='order_view'),
    path('order-cancel/<int:id>', views.order_cancel, name='order_cancel'),
    path('edit-status/<int:id>', views.edit_status, name='edit_status'),
    path('edit-months/<int:id>', views.ChangeMonthsView.as_view(), name='edit_months'),
    path('edit-staff-comment/<int:id>', views.edit_staff_comment, name='edit_staff_comment'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('account/', views.AccountVueView.as_view(), name='account'),
    
    path('staff/', views.StaffView.as_view(), name='staff'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('pre-pay/', views.PrePay.as_view(), name='pre_pay'),
    path('edit-address/', views.edit_address, name='edit_address'),
    path('edit-account/', views.edit_account, name='edit_account'),
    
    path('remove-from-cart/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('<int:pk>/car-item/delete/', views.DeleteFromCartView.as_view(), name='item_vuejs_delete'),
    path('<int:pk>/car-item/increase-qty/', views.IncreaseQtyCartView.as_view(), name='increase_qty'),
    path('<int:pk>/car-item/reduce-qty/', views.ReduceQtyCartView.as_view(), name='reduce_qty'),
    path('<int:month>/car-month-qty/', views.ChangeMonthsView.as_view(), name='chang_month_qty'),
    
]