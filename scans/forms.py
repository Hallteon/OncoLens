from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from scans.models import *
from users.models import CustomUser


class CreateScanRecordForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(CreateScanRecordForm, self).__init__(*args, **kwargs)
        self.fields['patient'] = forms.ModelChoiceField(label='Пациент', queryset=CustomUser.objects.get(id=user_id).patients.all(),
                                                empty_label='Не выбрано', widget=forms.Select(attrs={'class': 'form-select form__select'}))
        self.fields['base_image'].label = 'Исходный снимок'

    base_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control form-input form__input'}))
    tumor_diagnosed = forms.ChoiceField(label='Опухоль диагностирована', choices=[(None, 'Не выбрано'), (True, 'Да'), (False, 'Нет')],
                                        initial=None, widget=forms.Select(attrs={'class': 'form-select form__select'}))
    tumor_stage_doctor = forms.ModelChoiceField(label='Диагностированная стадия опухоли', queryset=TumorStage.objects.all(), required=False,
                                                empty_label='Опухоль отсутствует', widget=forms.Select(attrs={'class': 'form-select form__select'}))
    tumor_category_doctor = forms.ModelChoiceField(label='Диагностированная категория опухоли', queryset=TumorCategory.objects.all(), required=False,
                                                empty_label='Опухоль отсутствует', widget=forms.Select(attrs={'class': 'form-select form__select'}))
    axis = forms.ModelChoiceField(label='Ось снимка', queryset=ScanAxis.objects.all(), required=False,
                                                empty_label='Не выбрано', widget=forms.Select(attrs={'class': 'form-select form__select'}))

    class Meta:
        model = ScanRecord
        fields = ('base_image', 'tumor_diagnosed', 'tumor_stage_doctor', 'tumor_category_doctor', 'axis',
                  'patient')