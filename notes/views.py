# notes/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, LoginSerializer, NoteSerializer, ShareNoteSerializer, UpdateNoteSerializer, NoteHistorySerializer
from .models import Note, NoteHistory

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Here, you can generate and return an authentication token if needed
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_note(request):
    if request.user.is_authenticated:
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            note = Note.objects.create(owner=request.user, title=title, content=content)
            return Response({'message': 'Note created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_note(request, id):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(id=id)
            if request.user == note.owner or request.user in note.shared_with.all():
                serializer = NoteSerializer(note)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You do not have permission to view this note.'}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def share_note(request):
    if request.user.is_authenticated:
        serializer = ShareNoteSerializer(data=request.data)
        if serializer.is_valid():
            note_id = serializer.validated_data['note_id']
            users = serializer.validated_data['users']
            try:
                note = Note.objects.get(id=note_id)
                if request.user == note.owner:
                    shared_users = User.objects.filter(username__in=users)
                    for user in shared_users:
                        note.shared_with.add(user)
                    return Response({'message': 'Note shared successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'You do not have permission to share this note.'}, status=status.HTTP_403_FORBIDDEN)
            except Note.DoesNotExist:
                return Response({'error': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def update_note(request, id):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(id=id)
            if request.user == note.owner or request.user in note.shared_with.all():
                serializer = UpdateNoteSerializer(note, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Note updated successfully.'}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You do not have permission to update this note.'}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_note_version_history(request, id):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(id=id)
            if request.user == note.owner or request.user in note.shared_with.all():
                history_entries = NoteHistory.objects.filter(note=note)
                serializer = NoteHistorySerializer(history_entries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You do not have permission to view version history of this note.'}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found.'}, status=status)
