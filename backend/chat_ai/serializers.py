from rest_framework import serializers
from .models import ChatSession, ChatMessage, ChatContext
from users.serializers import UserProfileSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp', 'tokens_used']


class ChatContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatContext
        fields = ['id', 'context_type', 'context_data', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    contexts = ChatContextSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'title', 'created_at', 'updated_at', 'is_active', 'user', 'messages', 'contexts']


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100, required=False)
    include_context = serializers.BooleanField(default=True)


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    session_id = serializers.CharField()
    tokens_used = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
