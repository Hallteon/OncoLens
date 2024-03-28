from django.contrib import admin
from scans.models import *


class TumorStageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class TumorCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class ScanAxisAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'tumor_category_ai', 'tumor_stage_ai', 'tumor_category_doctor', 'tumor_stage_doctor',
                    'final_tumor_stage', 'final_tumor_category', 'tumor_diagnosed', 'tumor_predicted',
                    'predicted_probability', 'axis', 'by_user', 'patient', 'created_datetime',
                    'base_image', 'predicted_image')
    search_fields = ('id', 'patient', 'by_user')


admin.site.register(TumorStage, TumorStageAdmin)
admin.site.register(TumorCategory, TumorCategoryAdmin)
admin.site.register(ScanAxis, ScanAxisAdmin)
admin.site.register(ScanRecord, ScanRecordAdmin)
