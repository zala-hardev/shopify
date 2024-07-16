from re import template
from django.urls import path,include
from apps import views
# login and registration
from django.contrib.auth import views as auth_view
from .forms import CustomPasswordResetForm,MySetPasswordReset

urlpatterns = [
    path('',views.home_Page,name="home"),
    path('productDetails/<pk>',views.product_details,name="product_details"),
    path('contact/',views.contact,name="contact"),
    # path('login/',views.login_page,name="login"),
    path('cart/',views.add_cart_page,name="cart"),
    path('show-cart/',views.show_cart_page,name="show-cart"),
    path('plus-cart/',views.plus_cart),
    path('minus-cart/',views.minus_cart),
    path('remove-item-cart/',views.remove_cart),
    path('profile/',views.profile_page,name="profile"),

    # wishlist
    path('add-wishlist/',views.add_wishlist_items,name='add_to_wishlist'),
    # path('show-wishlist/',views.show_wishlist_items,name='show_wishlist'),

    path('shop-all/',views.shop_all_page,name="shop-all"),
    path('shop-mobile/',views.shop_mobile_page,name="shop-mobile"),
    path('shop-laptop/',views.shop_laptop_page,name="shop-laptop"),
    path('shop-smartwatch/',views.shop_smartwatch_page,name="shop-smartwatch"),
    path('shop-headphone/',views.shop_headphones_page,name="shop-headphone"),

    path('orders-all/',views.orders_all_page,name="orders-all"),
    path('orders/',views.orders_page,name="orders"),
    path('cancel-order/<cancel_id>',views.cancelled_order,name="cancel-order"),
    
    # for payment
    path('checkout/',views.checkout_page,name="checkout"),
    path('privacy-policy/',views.privacy_page,name="policy"),

    # login and signup and logout
    path('register/',views.signup_page,name="register"),
    path('accounts/login/',views.login_page,name="login"),
    path('accounts/login/auth/',include('social_django.urls', namespace='social')),
    # path('auth/', ),
    path('logout/',views.logout_page,name="logout"),

    # password change
    path('changepassword/',views.change_password,name="change_pass"),

    # forgot password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=CustomPasswordResetForm),name="password_reset"),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordReset),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    # generate pdf of invoice
    path('get_invoice/<payment_id>',views.invoice_pdf,name='generate_invoice'),

    path('admin_login/',views.admin_login_page,name="admin_login"),
    path('admin_login/dashboard',views.admin_dashboard,name="admin_dashboard"),
    path('admin_login/products',views.admin_product,name="admin_products"),
    path('admin_login/customers',views.admin_customers,name="admin_customers"),
    path('admin_login/show_products',views.admin_show_products,name="admin_show_products"),
    path('admin_login/delete_product',views.admin_delete_product,name="admin_delete_products"),

]   
