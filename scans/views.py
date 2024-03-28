from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from scans.forms import CreateScanRecordForm
from scans.models import TumorCategory, TumorStage, ScanRecord
from users.models import CustomUser
from utils.process_scan import ScanAIProcessor


class ShowHomePage(TemplateView):
    template_name = 'scans/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class ScanDetectView(LoginRequiredMixin, CreateView):

    form_class = CreateScanRecordForm
    template_name = 'scans/tumor_diagnosis.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ScanDetectView, self).get_form_kwargs()
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
        tumor_category = tumor_class[0]

        if not TumorCategory.objects.filter(name=tumor_category):
            cat = TumorCategory.objects.create(name=tumor_category)

            if len(tumor_class) == 2:
                tumor_stage = tumor_class[1]
                obj.tumor_stage_ai = TumorStage.objects.filter(name=tumor_stage)[0]

            obj.tumor_category_ai = cat

        else:
            if len(tumor_class) == 2:
                tumor_stage = tumor_class[1]

                if TumorStage.objects.filter(name=tumor_stage):
                    obj.tumor_stage_ai = TumorStage.objects.filter(name=tumor_stage)[0]

            if TumorCategory.objects.filter(name=tumor_category):
                obj.tumor_category_ai = TumorCategory.objects.filter(name=tumor_category)[0]

        obj.predicted_image = predicted_scan

        if tumor_category != '_NORMAL':
            obj.tumor_predicted = True
        else:
            obj.tumor_predicted = False

        obj.by_user = CustomUser.objects.get(pk=self.request.user.pk)

        obj.save()

        return redirect(obj.get_absolute_url())


class ScanShowView(DetailView):
    model = ScanRecord
    template_name = 'scans/scan_detail.html'
    pk_url_kwarg = 'scan_pk'
    context_object_name = 'scan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пересмотр снимка'

        return context


class UserScansShowView(ListView):
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



