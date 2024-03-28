class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs

        context['title'] = context['title']

        return context