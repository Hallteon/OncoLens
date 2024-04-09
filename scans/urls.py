from django.urls import path
from scans.views import *

urlpatterns = [
    path('', ShowHomePage.as_view(), name='home'),
    path('create/', ScanProcessView.as_view(), name='scan_create'),
    path('<int:scan_pk>/', ScanDetailView.as_view(), name='scan_detail'),
    path('my/', UserScansListView.as_view(), name='user_scans')
]