import uuid
import datetime
from django.db import models
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField

from users.models import Patient


class TumorStage(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стадия опухоли'
        verbose_name_plural = 'Стадии опухоли'


class TumorCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория опухоли'
        verbose_name_plural = 'Категории опухоли'


class ScanAxis(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ось снимка'
        verbose_name_plural = 'Оси снимка'


class ScanRecord(models.Model):
    base_image = models.ImageField(upload_to='scans/images/original/', blank=True, null=True,
                                   verbose_name='Оригинальный снимок')
    predicted_image = models.ImageField(blank=True, null=True, upload_to='scans/images/predicted/',
                                        verbose_name='Предсказанный снимок')
    tumor_stage_doctor = models.ForeignKey('TumorStage', blank=True, null=True, on_delete=models.DO_NOTHING,
                                           related_name='scans_doc_stage', verbose_name='Стадия (врач)')
    tumor_category_doctor = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                              related_name='scans_tumor_doc_category', verbose_name='Категория опухоли (врач)')
    tumor_stage_ai = models.ForeignKey('TumorStage', blank=True, null=True, on_delete=models.DO_NOTHING,
                                       related_name='scans_ai_stage', verbose_name='Стадия (ai)')
    tumor_category_ai = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_tumor_ai_category', verbose_name='Категория опухоли (ai)')
    final_tumor_stage = models.ForeignKey('TumorStage', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_final_stage', verbose_name='Финальная стадия')
    final_tumor_category = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_final_category', verbose_name='Финальная категория')
    tumor_diagnosed = models.BooleanField(blank=True, null=True, verbose_name='Опухоль диагностирована')
    tumor_predicted = models.BooleanField(blank=True, null=True, verbose_name='Опухоль предсказана')
    predicted_probability = models.FloatField(default=0, verbose_name='Вероятность наличия')
    axis = models.ForeignKey('ScanAxis', on_delete=models.DO_NOTHING, related_name='scans_axis', verbose_name='Ось')
    by_user = CurrentUserField(related_name='scans_author', verbose_name='Создатель')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scans_patient', verbose_name='Пациент')
    data = models.JSONField(blank=True, null=True, verbose_name='Данные')
    created_datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата создания')

    def __str__(self):
        return f'{self.created_datetime}'

    def get_absolute_url(self):
        return reverse('scan_detail', kwargs={'scan_pk': self.pk})

    class Meta:
        verbose_name = 'Запись о снимке'
        verbose_name_plural = 'Записи о снимках'
