import uuid
import datetime
from django.db import models
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField
from users.models import Patient


class TumorType(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    tumor_type = models.CharField(unique=True, max_length=255, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип опухоли'
        verbose_name_plural = 'Типы опухолей'


class TumorStage(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стадия опухоли'
        verbose_name_plural = 'Стадии опухоли'


class TumorCategory(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    tumor_type = models.ForeignKey('TumorType', on_delete=models.CASCADE, related_name='tumor_categories_tumor_type',
                                   verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория опухоли'
        verbose_name_plural = 'Категории опухоли'


class ScanType(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид снимка'
        verbose_name_plural = 'Вид снимка'


class ScanImage(models.Model):
    base_image = models.ImageField(upload_to='scans/images/base/', blank=True, null=True,
                                   verbose_name='Оригинальный снимок')
    processed_image = models.ImageField(blank=True, null=True, upload_to='scans/images/predicted/',
                                        verbose_name='Предсказанный снимок')
    structured_report = models.FileField(upload_to='scans/reports/', blank=True, null=True,
                                         verbose_name='DICOM-SR Отчёт')
    tumor_category_ai = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_images_tumor_category', verbose_name='Категория опухоли (ai)')
    predicted_probability = models.FloatField(default=0, verbose_name='Вероятность наличия')

    def __str__(self):
        return str(self.base_image)

    def get_absolute_url(self):
        return reverse('scan_image_detail', kwargs={'scan_image_pk': self.pk})

    class Meta:
        verbose_name = 'Снимок'
        verbose_name_plural = 'Снимки'


class ScanRecord(models.Model):
    scans = models.ManyToManyField('ScanImage', blank=True, related_name='scans_scan', verbose_name='Снимки')
    scan_type = models.ForeignKey('ScanType', related_name='scans_scan_type', on_delete=models.DO_NOTHING,
                                  verbose_name='Вид снимков')
    tumor_type = models.ForeignKey('TumorType', related_name='scans_tumor_type', on_delete=models.DO_NOTHING,
                                  verbose_name='Область опухоли')
    tumor_stage_doctor = models.ForeignKey('TumorStage', blank=True, null=True, on_delete=models.DO_NOTHING,
                                           related_name='scans_doc_stage', verbose_name='Стадия (врач)')
    tumor_category_doctor = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                              related_name='scans_tumor_doc_category', verbose_name='Категория опухоли (врач)')
    mean_tumor_category_ai = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_tumor_ai_category', verbose_name='Категория опухоли (ai)')
    final_tumor_stage = models.ForeignKey('TumorStage', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_final_stage', verbose_name='Финальная стадия')
    final_tumor_category = models.ForeignKey('TumorCategory', blank=True, null=True, on_delete=models.DO_NOTHING,
                                          related_name='scans_final_category', verbose_name='Финальная категория')
    tumor_diagnosed = models.BooleanField(blank=True, null=True, verbose_name='Опухоль диагностирована')
    tumor_predicted = models.BooleanField(blank=True, null=True, verbose_name='Опухоль предсказана')
    predicted_probability = models.FloatField(default=0, verbose_name='Вероятность наличия')
    by_user = CurrentUserField(related_name='scans_author', verbose_name='Создатель')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scans_patient', verbose_name='Пациент')
    data = models.JSONField(blank=True, null=True, verbose_name='Данные')
    created_datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата создания')

    def __str__(self):
        return f'{self.created_datetime}'

    def get_absolute_url(self):
        return reverse('scan_record_detail', kwargs={'scan_record_pk': self.pk})

    class Meta:
        verbose_name = 'Запись о снимке'
        verbose_name_plural = 'Записи о снимках'
