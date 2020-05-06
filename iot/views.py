from django.views.generic import TemplateView
from rfid.models import Item


class DashboardView(TemplateView):
    template_name = 'dashboard/logistics/logistics_index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        return context