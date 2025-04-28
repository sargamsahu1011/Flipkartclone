from django.urls import path, include  # Organize imports
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    # Home page
    path("", views.ProductView.as_view(), name="home"),

    # Product details and purchasing
    path("product-detail/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("buy/", views.buy_now, name="buy-now"),
    
    # User profile and address management
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path("orders/", views.orders, name="orders"),

    # Product categories
    path("mobile/", views.mobile, name="mobile"),
    path("mobile/<slug:data>/", views.mobile, name="mobiledata"),
    path("laptop/", views.laptop, name="laptop"),
    path("laptop/<slug:data>/", views.laptop, name="laptopdata"),
    
    path("menbottomwear/", views.menbottomwear, name="menbottomwear"),
    path("menbottomwear/<slug:data>/", views.menbottomwear, name="menbottomweardata"),
    path("mentopwear/", views.mentopwear, name="mentopwear"),
    path("mentopwear/<slug:data>/", views.mentopwear, name="mentopweardata"),
    
    path("womenbottomwear/", views.womenbottomwear, name="womenbottomwear"),
    path("womenbottomwear/<slug:data>/", views.womenbottomwear, name="womenbottomweardata"),
    path("womentopwear/", views.womentopwear, name="womentopwear"),
    path("womentopwear/<slug:data>/", views.womentopwear, name="womentopweardata"),
    
    path("boyswear/", views.boyswear, name="boyswear"),
    path("boyswear/<slug:data>/", views.boyswear, name="boysweardata"),
    path("girlswear/", views.girlswear, name="girlswear"),
    path("girlswear/<slug:data>/", views.girlswear, name="girlsweardata"),

    # Authentication URLs
    path("accounts/login/", auth_views.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name="login"),    
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    
    # Password management URLs
    path("passwordchange/", auth_views.PasswordChangeView.as_view(template_name="app/passwordchange.html", form_class=MyPasswordChangeForm, success_url="/passwordchangedone/"), name="passwordchange"),    
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name="passwordchangedone"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MyPasswordResetForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name="password_reset_complete"),

    # Cart management URLs
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
