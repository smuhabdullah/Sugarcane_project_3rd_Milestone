from django.urls import path

from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

# handler400 = 'uploads.views.page_not_found_view'
# handler403 = 'uploads.views.permission_denied'

# handler500 = 'uploads.views.server_error'



urlpatterns  = [
    path('',views.index, name='home'),
    path('about',views.about, name='about'),
    path('service',views.service, name='service'),
    path('prediction',views.prediction, name='prediction'),
    path('contact',views.contact, name='contact'),
    path('uploaded', views.uploaded, name = 'uploaded'),
    path('logout_Page', views.logout_Page, name = 'logout_Page'),
    path('user_profile', views.user, name = 'user'),
    path('404/', views.page_not_found_view),
    path('505/', views.server_error),
    path('change_password', views.change_pass, name = 'change_password'),
    path('disease_details/<str:disease>/', views.disease_details, name='disease_details'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
]

handler404 = 'uploads.views.page_not_found_view'
handler500 = 'uploads.views.server_error'