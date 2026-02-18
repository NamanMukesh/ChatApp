from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.

class RoomListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        return Room.objects.filter(users=self.request.user)


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        room_id=self.kwargs['room_id']
        
        return Message.objects.filter(
            room_id=room_id,
            room__users=self.request.user
        )

