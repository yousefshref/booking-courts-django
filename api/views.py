from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from django.db.models import Q
from datetime import datetime, timedelta


from . import serializers
from . import models


@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = models.CustomUser.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)



@api_view(['POST'])
def login(request):
    user = get_object_or_404(models.CustomUser, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("Something went wrong", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_states(request):
    states = models.State.objects.all()
    ser = serializers.StateSerializer(states, many=True)
    return Response(ser.data)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = models.CustomUser.objects.get(pk=request.user.pk)
    ser = serializers.UserSerializer(user)
    return Response(ser.data)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_courts(request):
    courts = models.Court.objects.all()

    search = request.GET.get('search')
    filter = request.GET.get('filter')

    if search:
        courts = courts.filter(title__icontains=search)

    if filter:
        courts = courts.filter(state__id=filter)


    ser = serializers.CourtSerializer(courts, many=True)
    return Response(ser.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court(request, pk):
    court = models.Court.objects.get(pk=pk)
    ser = serializers.CourtSerializer(court)
    return Response(ser.data)





def create_book_setting(book_id):
    book_setting = models.BookSetting(
        book_id=book_id
    )
    book_setting.save()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    ser = serializers.BookSerializer(data=request.data)
    if ser.is_valid():
        book = ser.save()
        create_book_setting(book.id)
        return Response(ser.data)
    return Response(ser.errors)








@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_book(request, court_id):
  book = models.Book.objects.filter(court__id=court_id)
  
  date = request.GET.get('date')

  if date:
      book = book.filter(Q(book_date=date))

  ser = serializers.BookSerializer(book, many=True)
  return Response(ser.data)
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_books(request, user_id):
    books = models.Book.objects.filter(user__id=user_id).order_by('-id')

    date = request.GET.get('date')

    if date:
        books = books.filter(book_date=date)

    ser = serializers.BookSerializer(books, many=True)
    return Response(ser.data)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book_setting(request, book_id):
    book = models.BookSetting.objects.get(book__id=book_id)
    ser = serializers.BookSettingSerializer(book)
    return Response(ser.data)
    


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_book_settings(request, book_id):
    book = models.BookSetting.objects.get(book__id=book_id)
    ser = serializers.BookSettingSerializer(book, data=request.data, partial=True)
    if ser.is_valid():
      ser.save()
      return Response(ser.data)
    return Response(ser.errors)







# get court tools
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court_additional_tools(request, court_id):
    tools = models.CourtAdditionalTool.objects.filter(court_additional__court__id=court_id)
    ser = serializers.CourtAdditionalToolSerializer(tools, many=True)
    return Response(ser.data)






