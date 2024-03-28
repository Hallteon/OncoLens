from django.urls import path
from users.views import *

urlpatterns = [
    path('account', ShowUserAccountView.as_view(), name='account'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]