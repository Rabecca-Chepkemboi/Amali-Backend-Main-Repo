from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from register.models import CustomUser, Athlete, Sponsor
from .serializers import CustomUserSerializer, AthleteSerializer, SponsorSerializer
from rest_framework import generics
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from donation.models import Donation
from .serializers import DonationSerializer, CommentSerializer
from comments.models import Comment
from contact.models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings

# from video.models import Video
# from .serializers import VideoSerializer


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='regular_user')
    serializer_class = CustomUserSerializer

class AthleteListView(generics.ListAPIView):
    queryset = Athlete.objects.filter(role='athlete')
    serializer_class = AthleteSerializer

class SponsorListView(generics.ListAPIView):
    queryset = Sponsor.objects.filter(role='sponsor')
    serializer_class = SponsorSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='regular_user')
    serializer_class = CustomUserSerializer
    lookup_field='id'

class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.filter(role='sponsor')
    serializer_class = SponsorSerializer
    lookup_field='id'

class AthleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Athlete.objects.filter(role="athlete")
    serializer_class = AthleteSerializer
    lookup_field='id'


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     role = request.data.get("role")
#     if role not in ['regular_user', 'athlete', 'sponsor']:
#         return Response({'message': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

#     if CustomUser.objects.filter(email=request.data.get('email')).exists():
#         return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

#     serializer = None
#     if role == 'regular_user':
#         serializer = CustomUserSerializer(data=request.data)
#     elif role == 'athlete':
#         serializer = AthleteSerializer(data=request.data)
#     elif role == 'sponsor':
#         serializer = SponsorSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         if isinstance(user, CustomUser):  
#             user.set_password(request.data.get('password'))
#             user.save()

#         return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    role = request.data.get("role")
    
    if role not in ['regular_user', 'athlete', 'sponsor']:
        return Response({'message': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = None
    
    if role == 'regular_user':
        serializer = CustomUserSerializer(data=request.data)
    elif role == 'athlete':
        serializer = CustomUserSerializer(data=request.data)
    elif role == 'sponsor':
        serializer = CustomUserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        
        if role == 'athlete':
            athlete = Athlete(
                age=request.data.get('age'),
                gender=request.data.get('gender'),
                full_name=request.data.get('full_name'),
                email=request.data.get('email'),
                password=request.data.get('password'),
                profile_picture=request.data.get('profile_picture'),
                achievements=request.data.get('achievements'),
                phone_number=request.data.get('phone_number'),
                role=request.data.get('role')
            )
            athlete.save()
        elif role == 'sponsor':
            sponsor = Sponsor(
                Bio=request.data.get('Bio'),
                full_name=request.data.get('full_name'),
                password=request.data.get('password'),
                phone_number=request.data.get('phone_number'),
                email=request.data.get('email'),
                Organisation=request.data.get('Organisation'),
                role=request.data.get('role')
            )
            sponsor.save()
        
        return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    if user.check_password(password):
        login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class DonationListView(APIView):
    def get(self, request):
        donations = Donation.objects.all()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

    def post(self, request):
        role = request.data.get("role")
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            donation = serializer.save()
            if role == 'athlete':
                athlete = Athlete.objects.create(
                    age=request.data.get('age'),
                    gender=request.data.get('gender'),
                    full_name=request.data.get('full_name'),
                    email=request.data.get('email'),
                    password=request.data.get('password'),
                    profile_picture=request.data.get('profile_picture'),
                    achievements=request.data.get('achievements'),
                    phone_number=request.data.get('phone_number'),
                    role=request.data.get('role')
                )
                donation.athlete = athlete
                donation.save()
            elif role == 'sponsor':
                sponsor = Sponsor.objects.create(
                    Bio=request.data.get('Bio'),
                    full_name=request.data.get('full_name'),
                    password=request.data.get('password'),
                    email=request.data.get('email'),
                    Organisation=request.data.get('Organisation'),
                    role=request.data.get('role')
                )
                donation.sponsor = sponsor
                donation.save()
            return Response({'message': 'Donation made successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonationDetailView(APIView):
    def get(self, request, id, format=None):
        donation = Donation.objects.get(id=id)
        serializer = DonationSerializer(donation)
        return Response(serializer.data)


    def put(self, request, id, format=None):
        donation = Donation.objects.get(id=id)
        serializer = DonationSerializer(donation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Donation updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id, format=None):
        donation = Donation.objects.get(id=id)
        donation.delete()
        return Response("Donation deleted", status=status.HTTP_204_NO_CONTENT)



class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentListAPIView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_comments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST'])
# def upload_video(request):
#     serializer = VideoSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'Video has been uploaded successfully.'}, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_all_videos(request):
#     videos = Video.objects.all()
#     serializer = VideoSerializer(videos, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET', 'PUT', 'DELETE'])
# def video_detail(request, pk):
#     try:
#         video = Video.objects.get(pk=pk)
#     except Video.DoesNotExist:
#         return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = VideoSerializer(video)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = VideoSerializer(video, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Video has been edited successfully.'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         video.delete()
#         return Response({'message': 'Video has been deleted.'}, status=status.HTTP_204_NO_CONTENT)



class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name', 'Anonymous')
            email = request.data.get('email', 'noreply@example.com')
            message = request.data.get('message', '')

            contact_message = serializer.save()

            subject = f'Message from {name}'
            email_message = f'\n\n{message}\n\n \n\n \n'

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactMessageListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer




