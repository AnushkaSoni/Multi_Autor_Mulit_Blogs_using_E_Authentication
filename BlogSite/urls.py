from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('change_user/',views.change_user,name="changeuser"),
    path('change_pass/',views.change_pass,name="changepass"),
    path('sendcode/',views.sendcode,name="sendcode"),
    path('verify_code/',views.verify_code,name="verify_code"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('signup/',views.signin,name="signup"),
    path('about/',views.about,name="about"),
    path('admin/', admin.site.urls),
    path('',views.index,name="main"),
    path('OTP/', views.OTPAuthentication,name="OTP_Authentication"),
    path('QR/',views.QRAuthentication,name="QR Authentication"),
 
    #Application urls included here
    path('blog/',include('blog.urls')),
    # path('chat/',include('chat.urls')),
    path('contact/',include('contact.urls')),
    # path('videochat/',include('videochat.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]