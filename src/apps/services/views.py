from django.db.models import Prefetch, Sum
from django.core.cache import cache
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.services.models import Subscription
from apps.services.serializsers import SubscriptionSerializer
from apps.clients.models import Client
from django.conf import settings


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().
                 select_related('user').only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.CACHED_PRICE_NAME)
        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.CACHED_PRICE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data,
                         'total_amount': total_price}
        response.data = response_data

        return response
