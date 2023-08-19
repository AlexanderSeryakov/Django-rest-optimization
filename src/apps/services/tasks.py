import time
from datetime import datetime

from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.core.cache import cache


@shared_task(base=Singleton)
def set_price(subscription_id):
    from apps.services.models import Subscription

    with transaction.atomic():
        subscription = (Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=(F('service__full_price') * (1 - F('plan__discount_percent') / 100.00)))).first()
        subscription.price = subscription.annotated_price
        subscription.save()

    cache.delete(settings.CACHED_PRICE_NAME)


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from apps.services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        subscription.comment = str(datetime.utcnow())
        subscription.save()

    cache.delete(settings.CACHED_PRICE_NAME)
