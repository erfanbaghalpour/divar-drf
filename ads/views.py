from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .models import Ad
from .serializers import AdSerializer
from rest_framework import status
from .pagination import StandardResultsSetPagination
from .permissions import IsPublisherOrReadOnly
from django.db.models import Q


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
    permission_classes = [IsAuthenticated, IsPublisherOrReadOnly]
    serializer_class = AdSerializer
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ad = self.get_object(pk)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdSearchView(APIView, StandardResultsSetPagination):
    """"ex: api/ads/search/?q=something"""
    serializer_class = AdSerializer

    def get(self, request):
        q = request.GET.get('q')
        queryset = Ad.objects.filter(Q(title=q) | Q(caption=q))
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializer(instance=result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
