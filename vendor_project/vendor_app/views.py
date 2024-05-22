from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .helper import get_tokens_for_user
from .serializers import *
from django.core.exceptions import ValidationError


# Create your views here.


# class UserSignupView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data': serializer.data, 'msg': "User created successfully"},
#                             status=status.HTTP_201_CREATED)
#         return Response({
#             "error": serializer.errors,
#             "msg": "Something went wrong"
#         }, status=status.HTTP_400_BAD_REQUEST)


# login views for all the users
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        is_user = authenticate(email=email, password=password)
        if is_user is not None:
            token = get_tokens_for_user(is_user)
            return Response({
                "email": is_user.email,
                "user_id": is_user.id,
                "access_token": token,
                "msg": "user login successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            "msg": "Unfortunately the credentials you are entering is not matching our records."
                   "Please try again later or try resetting the credentials"
        }, status=status.HTTP_400_BAD_REQUEST)


class VendorView(APIView):

    def post(self, request):
        data = request.data
        is_vendor = VendorDetail.objects.filter(full_name=data["full_name"]).first()
        if is_vendor is not None:
            return Response({"msg": "Vendor with this name already exists!"})
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "Vendor created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        vendors = VendorDetail.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class GetVendorView(APIView):

    def get(self, request, vendor_id):
        try:
            is_vendor = VendorDetail.objects.get(vendor_code=vendor_id)

        except VendorDetail.DoesNotExist:
            return Response({"msg": f"Vendor with this vendor_code: {vendor_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"msg": f"Invalid vendor code: {vendor_id}"}, status=status.HTTP_400_BAD_REQUEST)

        vendor = VendorSerializer(is_vendor)
        return Response({"data": vendor.data}, status=status.HTTP_200_OK)

    def put(self, request, vendor_id):
        try:
            is_vendor = VendorDetail.objects.get(vendor_code=vendor_id)

        except VendorDetail.DoesNotExist:
            return Response({"msg": f"Vendor with this vendor_code: {vendor_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"msg": f"Invalid vendor code: {vendor_id}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VendorSerializer(is_vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "vendor updated successfully"}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        try:
            is_vendor = VendorDetail.objects.get(vendor_code=vendor_id)

        except VendorDetail.DoesNotExist:
            return Response({"msg": f"Vendor with this vendor_code: {vendor_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"msg": f"Invalid vendor code: {vendor_id}"}, status=status.HTTP_400_BAD_REQUEST)

        is_vendor.delete()
        return Response({"msg": "Vendor deleted successfully!"}, status=status.HTTP_200_OK)


class PurchaseOrderView(APIView):

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order_date=timezone.now())
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        try:
            if request.data:
                orders = PurchaseOrder.objects.filter(vendor=request.data["vendor"])
                if orders:
                    serializer = PurchaseOrderSerializer(orders, many=True)
                    return Response({"data": serializer.data}, status=status.HTTP_200_OK)

                return Response({"msg": "No Purchase Order with this vendor"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": "Invalid vendor_code"}, status=status.HTTP_400_BAD_REQUEST)

        PO = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(PO, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class GetPurchaseOrderView(APIView):
    def get(self, request, po_id):
        try:
            data = PurchaseOrder.objects.get(po_number=po_id)

        except PurchaseOrder.DoesNotExist:
            return Response({"msg": f"No Purchase Order with this PO_number: {po_id}"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": f"Invalid vendor_code: {po_id}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PurchaseOrderSerializer(data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, po_id):
        try:
            data = PurchaseOrder.objects.get(po_number=po_id)

        except PurchaseOrder.DoesNotExist:
            return Response({"msg": f"No Purchase Order with this PO_number: {po_id}"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": f"Invalid PO_number: {po_id}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PurchaseOrderSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "Purchase order updated successfully!"}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        try:
            data = PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"msg": f"No Purchase Order with this PO_number: {po_id}"},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": f"Invalid PO_number: {po_id}"}, status=status.HTTP_400_BAD_REQUEST)

        data.delete()
        return Response({"msg": "Purchase order deleted successfully!"}, status=status.HTTP_200_OK)


class UpdateAcknowledgmentView(APIView):
    def post(self, request, po_id):
        try:
            data = PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"msg": f"No Purchase Order with this PO_number: {po_id}"},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": f"Invalid PO_number: {po_id}"}, status=status.HTTP_400_BAD_REQUEST)

        data.acknowledgment_date = timezone.now()
        data.save()
        return Response({"msg": "Acknowledgement saved successfully!"}, status=status.HTTP_200_OK)


class GetVendorPerformance(APIView):
    def get(self, request, vendor_id):
        try:
            historical_data = HistoricalPerformance.objects.get(vendor=vendor_id)

        except HistoricalPerformance.DoesNotExist:
            return Response({"msg": f"No Historical data with this Vendor id: {vendor_id}"},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"msg": f"Invalid Vendor id: {vendor_id}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HistoricalPerformanceSerializer(historical_data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
