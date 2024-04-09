from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from scans.forms import CreateScanRecordForm, SelectFinalScanDiagnosisForm
from scans.models import TumorCategory, TumorStage, ScanRecord
from scans.services.scans_service import ScanRecordProcessService
from users.models import CustomUser
from django.views.generic.edit import FormMixin
from utils.process_scan import ScanAIProcessor


class ShowHomePage(TemplateView):
    template_name = 'scans/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class ScanProcessView(LoginRequiredMixin, CreateView):
    form_class = CreateScanRecordForm
    template_name = 'scans/scan_create.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ScanProcessView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обработка снимка'

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        process_scan = ScanAIProcessor(obj.pk, obj.base_image)
        predicted_scan = process_scan.detect_tumor()
        tumor_class = process_scan.classify_tumor().split(' ')

        ScanRecordProcessService(self.request.user.id, {'predicted_scan': predicted_scan,
                                                       'tumor_class': tumor_class}, obj.id).execute()

        return redirect(obj.get_absolute_url())


class ScanDetailView(FormMixin, DetailView):
    model = ScanRecord
    form_class = SelectFinalScanDiagnosisForm
    template_name = 'scans/scan_detail.html'
    pk_url_kwarg = 'scan_pk'
    context_object_name = 'scan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пересмотр снимка'

        return context

    def get_success_url(self):
        return reverse_lazy('user_scans')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.final_tumor_stage = form.cleaned_data['final_tumor_stage']
        instance.final_tumor_category = form.cleaned_data['final_tumor_category']
        instance.id = self.get_object().id

        instance.save(update_fields=['final_tumor_stage', 'final_tumor_category'])

        return super(ScanDetailView, self).form_valid(form)


class UserScansListView(ListView):
    model = ScanRecord
    template_name = 'scans/user_scans.html'
    context_object_name = 'scans'
    paginate_by = None

    def get_queryset(self):
        return ScanRecord.objects.filter(by_user=self.request.user).order_by('-created_datetime')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Снимки пользователя'

        return context

