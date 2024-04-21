from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from scans.models import *
from users.models import CustomUser


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control form-input form__input'}))
        kwargs.setdefault('label', 'Images')
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateScanRecordForm(forms.ModelForm):
    def __init__(self, user_id, tumor_type, *args, **kwargs):
        super(CreateScanRecordForm, self).__init__(*args, **kwargs)
        self.fields['patient'] = forms.ModelChoiceField(label='Пациент', queryset=CustomUser.objects.get(id=user_id).patients.all(),
                                                empty_label='Не выбрано', widget=forms.Select(attrs={'class': 'form-select form__select'}))
        self.fields['tumor_category_doctor'] = forms.ModelChoiceField(label='Категория опухоли (врач)',
                                                      queryset=TumorCategory.objects.filter(
                                                      tumor_type__tumor_type=f'{tumor_type}_tumor'),
                                                      required=False,
                                                      empty_label='Отсутствует',
                                                      widget=forms.Select(attrs={'class': 'form-select form__select'}))

    scan_files = MultipleFileField()
    scan_type = forms.ModelChoiceField(label='Тип снимка', queryset=ScanType.objects.all(), required=False,
                                       empty_label='Не выбрано',
                                       widget=forms.Select(attrs={'class': 'form-select form__select'}))
    tumor_stage_doctor = forms.ModelChoiceField(label='Стадия опухоли (врач)',
                                                queryset=TumorStage.objects.all(), required=False,
                                                empty_label='Отсутствует',
                                                widget=forms.Select(attrs={'class': 'form-select form__select'}))

    class Meta:
        model = ScanRecord
        fields = ('scan_files', 'scan_type', 'tumor_stage_doctor', 'tumor_category_doctor',
                  'patient')


class SelectFinalScanDiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SelectFinalScanDiagnosisForm, self).__init__(*args, **kwargs)

        if kwargs.get('initial', None):
            self.fields['final_tumor_category'] = forms.ModelChoiceField(label='Категория опухоли после пересмотра',
                                                                         queryset=TumorCategory.objects.filter(
                                                                             tumor_type=kwargs['initial'].get(
                                                                                 'tumor_type')),
                                                                         required=False,
                                                                         empty_label='Отсутствует',
                                                                         widget=forms.Select(attrs={
                                                                             'class': 'form-select form__select'}))

        else:
            self.fields['final_tumor_category'] = forms.ModelChoiceField(label='Категория опухоли после пересмотра',
                                                                         queryset=TumorCategory.objects.all(),
                                                                         required=False,
                                                                         empty_label='Отсутствует',
                                                                         widget=forms.Select(attrs={
                                                                             'class': 'form-select form__select'}))

    final_tumor_stage = forms.ModelChoiceField(label='Стадия опухоли после пересмотра',
                                                queryset=TumorStage.objects.all(), required=False,
                                                empty_label='Отсутствует',
                                                widget=forms.Select(attrs={'class': 'form-select form__select'}))

    class Meta:
        model = ScanRecord
        fields = ('final_tumor_stage', 'final_tumor_category')


class AddScanImageForm(forms.ModelForm):
    scan_files = MultipleFileField(label='Дополнительные снимки')

    class Meta:
        model = ScanImage
        fields = ('scan_files',)
