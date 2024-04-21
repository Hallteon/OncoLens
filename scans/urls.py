from django.urls import path
from scans.views import *

urlpatterns = [
    path('', ShowHomePage.as_view(), name='home'),
    path('create/<str:tumor_type>/', ScanRecordCreateView.as_view(), name='scan_create'),
    path('<int:scan_record_pk>/', ScanRecordDetailView.as_view(), name='scan_record_detail'),
    path('images/<int:scan_image_pk>/', ScanImageDetailView.as_view(), name='scan_image_detail'),
    path('my/<str:tumor_type>/', UserScanRecordsListView.as_view(), name='user_scans')
]