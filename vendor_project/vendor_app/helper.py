from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg, Count, ExpressionWrapper, F, fields, Q
from django.utils import timezone
from .models import *

# this function is used to generate the tokens for authorization
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def update_historical_performance(vendor_id):
    vendor = VendorDetail.objects.get(vendor_code=vendor_id)
    now = timezone.now()

    # Calculate metrics
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)

    if purchase_orders.exists():
        total_orders = purchase_orders.count()
        on_time_deliveries = purchase_orders.filter(delivery_date__lte=F('order_date') + timezone.timedelta(days=7)).count()
        on_time_delivery_rate = (on_time_deliveries / total_orders) * 100

        quality_rating_avg = purchase_orders.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0

        avg_response_time = purchase_orders.annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('order_date'), output_field=fields.DurationField())
        ).aggregate(avg_response=Avg('response_time'))['avg_response'].total_seconds() or 0

        avg_response_time_hours = avg_response_time / 3600 if avg_response_time else 0

        fulfilled_orders = purchase_orders.filter(status="COMPLETED").count()
        fulfillment_rate = (fulfilled_orders / total_orders) * 100

        try:
            data = HistoricalPerformance.objects.get(vendor=vendor)
            if data:
                HistoricalPerformance.objects.update(
                    vendor=vendor,
                    date=now,
                    on_time_delivery_rate=on_time_delivery_rate,
                    quality_rating_avg=quality_rating_avg,
                    average_response_time=avg_response_time_hours,
                    fulfillment_rate=fulfillment_rate
                )
        except HistoricalPerformance.DoesNotExist:
            # No purchase orders, set default values
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=now,
                on_time_delivery_rate=0,
                quality_rating_avg=0,
                average_response_time=0,
                fulfillment_rate=0
            )
