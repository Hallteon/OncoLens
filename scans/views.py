from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, resolve
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from scans.forms import CreateScanRecordForm, SelectFinalScanDiagnosisForm, AddScanImageForm
from scans.models import TumorCategory, TumorStage, ScanRecord, TumorType, ScanImage
from scans.services.scan_images_service import ScanImageProcessService
from scans.services.scan_records_service import ScanRecordPService
from statistics import mode
from django.views.generic.edit import FormMixin
from utils.process_scan import ScanAIProcessor


class ShowHomePage(TemplateView):
    template_name = 'scans/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class ScanRecordCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateScanRecordForm
    template_name = 'scans/scan_create.html'
    success_url = reverse_lazy('user_scans')

    def get_form_kwargs(self):
        kwargs = super(ScanRecordCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        kwargs['tumor_type'] = self.kwargs.get('tumor_type')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание записи'

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.by_user = self.request.user
        tumor_type = self.kwargs.get('tumor_type')

        if tumor_type == 'brain':
            obj.tumor_type = TumorType.objects.get(tumor_type='brain_tumor')
        elif tumor_type == 'lung':
            obj.tumor_type = TumorType.objects.get(tumor_type='lung_tumor')

        if obj.tumor_category_doctor:
            obj.tumor_diagnosed = True

        else:
            obj.tumor_diagnosed = False

        obj.save()

        scans = form.cleaned_data['scan_files']
        processed_scans = []
        predicted_classes = []

        for index, scan in enumerate(scans):
            process_scan = ScanAIProcessor(f'{obj.pk}_{index}', scan, tumor_type)
            predicted_scan = process_scan.detect_tumor()
            tumor_class = process_scan.classify_tumor()

            scan_image = ScanImageProcessService(self.request.user.id,
                                                 {'base_image': scan, 'predicted_scan': predicted_scan,
                                                  'tumor_class': tumor_class, 'tumor_type': f'{tumor_type}_tumor'}).create_scan_image()
            processed_scans.append(scan_image.pk)
            predicted_classes.append(tumor_class)

        scan_record = ScanRecordPService(self.request.user.pk, obj.pk)
        scan_record.add_scan_images(processed_scans)
        scan_record.set_tumor_category(mode(predicted_classes))

        return redirect(obj.get_absolute_url())


class ScanImageDetailView(LoginRequiredMixin, DetailView):
    model = ScanImage
    template_name = 'scans/scan_detail.html'
    pk_url_kwarg = 'scan_image_pk'
    context_object_name = 'scan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Снимок №{self.get_object().pk}'

        return context

    def get_success_url(self):
        return reverse_lazy('user_scans')


class UserScanRecordsListView(LoginRequiredMixin, ListView):
    model = ScanRecord
    template_name = 'scans/user_scan_records.html'
    context_object_name = 'scan_records'
    paginate_by = None

    def get_queryset(self):
        tumor_type = self.kwargs.get('tumor_type')

        return ScanRecord.objects.filter(by_user=self.request.user, tumor_type__tumor_type=f'{tumor_type}_tumor').order_by('-created_datetime')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Снимки пользователя'
        context['tumor_type'] = self.kwargs.get('tumor_type')

        return context


class ScanRecordDetailView(LoginRequiredMixin, DetailView):
    model = ScanRecord
    template_name = 'scans/scan_record_detail.html'
    pk_url_kwarg = 'scan_record_pk'
    context_object_name = 'scan_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пересмотр записи снимков'
        context['select_diagnosis_form'] = SelectFinalScanDiagnosisForm(initial={'tumor_type': self.get_object().tumor_type})
        context['add_scans_form'] = AddScanImageForm()

        return context

    def post(self, request, *args, **kwargs):
        select_diagnosis_form = SelectFinalScanDiagnosisForm(self.request.POST)
        add_scans_form = AddScanImageForm(self.request.POST, request.FILES)

        if add_scans_form.is_valid() and self.request.FILES:
            scans = add_scans_form.cleaned_data['scan_files']
            processed_scans = []
            predicted_classes = []

            for index, scan in enumerate(scans):
                process_scan = ScanAIProcessor(f'{self.get_object().pk}_{index}', scan,
                                               self.get_object().tumor_type.tumor_type.split('_')[0])
                predicted_scan = process_scan.detect_tumor()
                tumor_class = process_scan.classify_tumor()

                scan_image = ScanImageProcessService(self.request.user.id,
                                                     {'base_image': scan, 'predicted_scan': predicted_scan,
                                                      'tumor_class': tumor_class, 'tumor_type': self.get_object().tumor_type.tumor_type}).create_scan_image()
                processed_scans.append(scan_image.pk)
                predicted_classes.append(tumor_class)

            scan_record = ScanRecordPService(self.request.user.pk, self.get_object().pk)
            scan_record.add_scan_images(processed_scans)
            scan_record.set_tumor_category(mode(predicted_classes))

            return redirect(self.get_object().get_absolute_url())

        if select_diagnosis_form.is_valid():
            instance = select_diagnosis_form.save(commit=False)
            instance.final_tumor_stage = select_diagnosis_form.cleaned_data['final_tumor_stage']
            instance.final_tumor_category = select_diagnosis_form.cleaned_data['final_tumor_category']
            instance.id = self.get_object().id

            instance.save(update_fields=['final_tumor_stage', 'final_tumor_category'])

            return redirect(self.get_object().get_absolute_url())

    def get_success_url(self):
        return reverse_lazy('user_scans')
