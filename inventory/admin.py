from django.contrib import admin
from django.apps import apps

# Register all Models to admin
app = apps.get_app_config('inventory')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass