from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api.views import logout_user, registration_view

urlpatterns = [
    #gives access to token/gives token when i send username and login as post to this link
    path('login/',obtain_auth_token,name = 'login'),
    path('register/',registration_view, name = 'register'),
    path('logout/',logout_user, name = 'logout'),
]