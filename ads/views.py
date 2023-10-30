from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
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


class AdCreateView(APIView):
    serializer_class = AdSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdDetailView(APIView):
    serializer_class = AdSerializer

    def get(self, request, pk):
        instance = Ad.objects.get(id=pk)
        serializer = AdSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
