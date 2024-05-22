from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorView.as_view(), name="Vendor"),
    path('vendors/<str:vendor_id>/', GetVendorView.as_view(), name="Vendor-with-code"),
    path('purchase_orders/', PurchaseOrderView.as_view(), name="Purchase-Orders"),
    path('purchase_orders/<str:po_id>', GetPurchaseOrderView.as_view(), name="Get-PO-with-number"),
    path('purchase_orders/<str:po_id>/acknowledge', UpdateAcknowledgmentView.as_view(), name="Update-Ack-PO-with-number"),
    path('vendors/<str:vendor_id>/performance', GetVendorPerformance.as_view(), name="Get-vendor-performance-by-id"),

]
