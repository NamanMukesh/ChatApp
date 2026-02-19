from django.urls import path    
from django.urls import path    
from .views import RoomListView, MessageListView, index, chat

urlpatterns = [
    path('', index, name='index'),
    path('chat/', chat, name='chat'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),
]
