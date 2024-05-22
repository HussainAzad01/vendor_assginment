from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VendorDetail, PurchaseOrder
from django.db.models import Avg, F, ExpressionWrapper, fields
from .helper import update_historical_performance
from datetime import timedelta


# def calculate_average_response_time(po_id):
#     # Filter requests by the vendor
#     purchase_requests = PurchaseOrder.objects.filter(po_number=po_id)
#
#     # Calculate the average response time
#     avg_response_time = purchase_requests.annotate(
#         response_time=ExpressionWrapper(F('acknowledgment_date') - F('order_date'), output_field=fields.DurationField())
#     ).aggregate(avg_response_time=Avg('response_time'))
#
#     return avg_response_time['avg_response_time']

@receiver(post_save, sender=PurchaseOrder)
def update_perform_metrics(sender, instance, created, **kwargs):
    if not created:

        update_historical_performance(instance.vendor.vendor_code)


