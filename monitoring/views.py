from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.utils.timezone import now

from .models import Keyword, Flag
from .serializers import KeywordSerializer, FlagSerializer
from monitoring.services.scanner import run_scan

@api_view(['POST'])
def create_keyword(request):
    serializer = KeywordSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def run_scan_api(request):
    run_scan()
    return Response({"message": "Scan completed"})


@api_view(['GET'])
def list_flags(request):
    flags = Flag.objects.all().order_by('-id')
    serializer = FlagSerializer(flags, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_flag_status(request, id):
    try:
        flag = Flag.objects.get(id=id)
    except Flag.DoesNotExist:
        return Response({"error": "Flag not found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')

    if new_status not in ['pending', 'relevant', 'irrelevant']:
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    flag.status = new_status

    if new_status in ['relevant', 'irrelevant']:
        flag.reviewed_at = now()
    flag.save()

    return Response({"message": "Status updated"})