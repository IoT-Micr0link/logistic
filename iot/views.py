from django.views import generic


class DashboardView(generic.TemplateView):
    template_name = 'dashboard/logistica/index_logistica.html'