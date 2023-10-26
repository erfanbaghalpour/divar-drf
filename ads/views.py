from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ad
from .serializers import AdSerializer
from rest_framework import status
from .pagination import StandardResultsSetPagination

class AdListView(APIView, StandardResultsSetPagination):
    serializer_class = AdSerializer
    def get(self, request):
        queryset = Ad.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializer(instance=result, many=True)
        return self.get_paginated_response(serializer.data)
