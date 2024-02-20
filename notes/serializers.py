# notes/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'owner', 'title', 'content', 'shared_with')

class ShareNoteSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()
    users = serializers.ListField(child=serializers.CharField())

class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('content',)

class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = ('timestamp', 'user', 'change_description')
