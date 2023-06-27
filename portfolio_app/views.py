from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from portfolio_app.models import MyUser, Project, Comment, Like, Contact
from portfolio_app.serializers import ProjectSerializer, CommentSerializer, LikeSerializer, ContactSerializer

from django.shortcuts import render
from django.template.loader import render_to_string

import sendgrid
from sendgrid.helpers.mail import * 
from decouple import config 


# Create your views here.
def landing(request):
    title = 'welcome'
    return render(request,'landing.html',{"title":title,})

def home(request):
    title = 'home'
    projects = Project.objects.all()
    comments = Comment.objects.all()
    return render(request,'index.html',{"title":title,"projects":projects,"comments":comments,})

@permission_classes([AllowAny,])
class AllProjects(APIView):
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializers = ProjectSerializer(projects,many=True)
        return Response(serializers.data)
    
@permission_classes([AllowAny,])
class ProjectDetails(APIView):    
    def get(self, request, id, format=None):
        project = Project.objects.all().filter(pk=id).last()
        serializers = ProjectSerializer(project,many=False)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class AddProject(APIView):
    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

@permission_classes([AllowAny,])
class ProjectLikes(APIView):    
    def get(self, request, id, format=None):
        likes = Like.objects.all().filter(project=id)
        serializers = LikeSerializer(likes,many=True)
        return Response(serializers.data)

@permission_classes([AllowAny,])
class ProjectComments(APIView):    
    def get(self, request, id, format=None):
        comments = Comment.objects.all().filter(project=id)
        serializers = CommentSerializer(comments,many=True)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class UpdateProject(APIView):
    def put(self, request, id, format=None):
        project = Project.objects.all().filter(pk=id).last()
        serializers = ProjectSerializer(project,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        project = Project.objects.all().filter(pk=id).last()
        project.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([AllowAny,])
class AllComments(APIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializers = CommentSerializer(comments,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid():
            comment = serializers.validated_data['comment']
            commented_by = serializers.validated_data['commented_by']
            project = serializers.validated_data['project']
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/comment-new.html', {
                'comment': comment,
                'commented_by': commented_by,
                "project": project,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'fullstack.benie@gmail.com',
                subject = "New Contact",
                html_content= msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 


@permission_classes([AllowAny,])
class CommentDetails(APIView):    
    def get(self, request, id, format=None):
        comment = Comment.objects.all().filter(pk=id).last()
        serializers = CommentSerializer(comment,many=False)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class DeleteComment(APIView):
    def delete(self, request, id, format=None):
        comment = Comment.objects.all().filter(pk=id).last()
        comment.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([AllowAny,])
class AllLikes(APIView):
    def get(self, request, format=None):
        likes = Like.objects.all()
        serializers = LikeSerializer(likes,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LikeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

@permission_classes([AllowAny,])
class LikeDetails(APIView):    
    def get(self, request, id, format=None):
        like = Like.objects.all().filter(pk=id).last()
        serializers = LikeSerializer(like,many=False)
        return Response(serializers.data)
    
@permission_classes([IsAdminUser,])
class DeleteLike(APIView):
    def delete(self, request, id, format=None):
        like = Like.objects.all().filter(pk=id).last()
        like.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAdminUser,])
class AllContacts(APIView):
    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializers = ContactSerializer(contacts,many=True)
        return Response(serializers.data)

@permission_classes([AllowAny,])
class AddContact(APIView):
    def post(self, request, format=None):
        serializers = ContactSerializer(data=request.data)
        if serializers.is_valid():
            name = serializers.validated_data['name']
            email = serializers.validated_data['email']
            message = serializers.validated_data['message']
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/contact-new.html', {
                'name': name,
                'email': email,
                "message": message,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'fullstack.benie@gmail.com',
                subject = "New Contact",
                html_content= msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)

            msg2 = render_to_string('email/contact-msg-delivered.html', {
                'name': name,
            })
            message2 = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = email,
                subject = "Message Delivered",
                html_content= msg2
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message2)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

@permission_classes([IsAdminUser,])
class ContactDetails(APIView):    
    def get(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        serializers = ContactSerializer(contact,many=False)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class DeleteContact(APIView):
    def delete(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 