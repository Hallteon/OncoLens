from django.contrib import admin
from scans.models import *


class TumorStageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class TumorCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class TumorTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class ScanTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class ScanImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'tumor_category_ai', 'predicted_probability',
                    'structured_report', 'base_image', 'processed_image')
    search_fields = ('id', 'tumor_category_ai', 'predicted_probability')


class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan_type', 'mean_tumor_category_ai', 'tumor_category_doctor', 'tumor_stage_doctor',
                    'final_tumor_stage', 'final_tumor_category', 'tumor_diagnosed', 'tumor_predicted',
                    'predicted_probability', 'by_user', 'patient', 'created_datetime')
    search_fields = ('id', 'patient', 'by_user')


admin.site.register(ScanImage, ScanImageAdmin)
admin.site.register(TumorType, TumorTypeAdmin)
admin.site.register(TumorStage, TumorStageAdmin)
admin.site.register(TumorCategory, TumorCategoryAdmin)
admin.site.register(ScanRecord, ScanRecordAdmin)
admin.site.register(ScanType, ScanTypeAdmin)