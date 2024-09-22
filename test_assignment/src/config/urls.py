from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from core.views import Handler404, Handler500, Handler403, Handler502, Handler503


urlpatterns = [

    # Django Admin and Jet URLS
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("jet/", include("jet.urls", "jet")),
    path("admin/", admin.site.urls),

    # Main URL
    path("", include("core.urls", namespace="core")),

    # Subscription URL
    path("subscriptions/", include("subscriptions.urls", namespace="subscriptions")),

    # API URL
    path("api-auth/", include("rest_framework.urls")),

    # Prometheus URL
    path("", include("django_prometheus.urls")),

    # Account URL
    path("account/", include("account.urls", namespace="account")),

    # Password reset views
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = Handler403.as_view()
handler404 = Handler404.as_view()
handler500 = Handler500.as_view()
handler502 = Handler502.as_view()
handler503 = Handler503.as_view()


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
