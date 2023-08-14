from django.contrib import admin
from apps.services import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'plan', 'price')


admin.site.register(models.Service)
admin.site.register(models.Plan)
admin.site.register(models.Subscription, SubscriptionAdmin)
