from django.urls import path
from scans.views import *

urlpatterns = [
    path('', ShowHomePage.as_view(), name='home'),
    path('tumor/diagnosis/', ScanDetectView.as_view(), name='diagnosis'),
    path('tumor/<int:scan_pk>/', ScanShowView.as_view(), name='scan_detail'),
    path('tumor/my/', UserScansShowView.as_view(), name='user_scans')
]