from django.views import generic
from rfid.models import Item


class DashboardView(generic.TemplateView):
    template_name = 'dashboard/logistica/index_logistica.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        return context