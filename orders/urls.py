from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add_cart/<int:product_id>/<int:size_id>/', views.AddCartView.as_view(), name='add_cart'),
    path('deletecart/<int:size_id>/', views.DeleteCartView.as_view(), name='delete_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('ecpay/', views.ECPayView.as_view(), name='ecpay'),
    path('return/', views.ReturnView.as_view(), name='return'),
    path('orderresult/', views.OrderResultView.as_view(), name='orderresult'),
    path('order_success/', views.OrderSuccessView.as_view(), name='order_success'),
    path('order_fail/', views.OrderFailView.as_view(), name='order_fail'),
    path('search_orders/', views.SearchOrders.as_view(), name='search_orders'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('update-cart/', views.UpdateCartView.as_view(), name='update_cart'),
    path('delete-cart/<int:size_id>/', views.DeleteCartView.as_view(), name='delete_cart'),
]