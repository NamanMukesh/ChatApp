from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class RoomListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        return Room.objects.filter(users=self.request.user)


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    
    def get_queryset(self):
        room_id=self.kwargs['room_id']
        
        return Message.objects.filter(
            room_id=room_id,
            room__users=self.request.user
        ).order_by('-created_at')

class MessageSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('search', '').strip()

        if not query:
            return Response([])

        messages = Message.objects.filter(
            room__users=request.user,
            content__icontains=query
        ).order_by('created_at')

        serializer = MessageSerializer(messages, many = True)
        return Response(serializer.data)        


def index(request):
    return render(request, 'Chat/index.html')

def chat(request):
    return render(request, 'Chat/chat.html')
