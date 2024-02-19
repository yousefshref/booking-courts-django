from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import F, Q

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

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
    courts = models.Court.objects.all().order_by('-id')

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


# admin
def create_additional_tools(additional_id, tools):
    tools_loaded = json.loads(tools)
    for i in tools_loaded:
        tool = models.CourtAdditionalTool(
          court_additional_id=additional_id,
          title=i['title'],
          price=i['price'],
        )
        tool.save()
    
def create_court_additional(user_id, court_id, tools):
    court_additional = models.CourtAdditional(
        user_id=user_id,
        court_id=court_id,
    )
    court_additional.save()
    create_additional_tools(court_additional.pk, tools)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court(request):
    ser = serializers.CourtSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        create_court_additional(ser.data['user'], ser.data['id'], request.data['tools'])
        return Response(ser.data)
    return Response(ser.errors)




def update_additional_tools(court_id, tools):

    additional = models.CourtAdditional.objects.get(court__pk=court_id)

    new_tools = json.loads(tools)
    old_tools = models.CourtAdditionalTool.objects.filter(court_additional__court__pk=court_id)
    
    tools_to_delete = []

    for old_tool in old_tools:
        tool_exists = False
        for new_tool in new_tools:
            if new_tool['title'] == old_tool.title:
                tool_exists = True
                if new_tool['price'] != old_tool.price:
                    old_tool.price = new_tool['price']
                    old_tool.save()
                break

        if not tool_exists:
            tools_to_delete.append(old_tool.id)

    models.CourtAdditionalTool.objects.filter(id__in=tools_to_delete).delete()

    for new_tool in new_tools:
        tool_exists = False
        for old_tool in old_tools:
            if new_tool['title'] == old_tool.title:
                tool_exists = True
                break

        if not tool_exists:
            models.CourtAdditionalTool.objects.create(
                court_additional_id=additional.pk,
                title=new_tool['title'],
                price=new_tool['price']
            )
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_court(request, court_id):
    court = models.Court.objects.get(id=court_id)
    ser = serializers.CourtSerializer(court, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        update_additional_tools(ser.data['id'], request.data['tools'])
        return Response(ser.data)
    return Response(ser.errors)






def create_book_setting(book_id):
    book_setting = models.BookSetting(
        book_id=book_id
    )
    book_setting.save()

def create_book_times(book_id, times):
    for i in times:
        print(i)
        instance = models.BookTime(
          book_id=book_id,
          book_from=i['book_from'],
          book_to=i['book_to']
        )
        instance.save()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    ser = serializers.BookSerializer(data=request.data)
    if ser.is_valid():
        book = ser.save()
        create_book_setting(book.id)
        create_book_times(book.id, request.data['book_time'])
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


# admin
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_books(request):
    if request.user.is_superuser:
        books = models.Book.objects.all().order_by('-id')
        date = request.GET.get('date')
        search = request.GET.get('search')

        if date:
            # Filter based on book_date and book_to
            books = books.filter(
                Q(book_date=date) | 
                Q(booksetting__book_to=date) |
                (Q(book_date__lte=date) & Q(booksetting__book_to__gte=date))
            )

        if search:
            books = books.filter(Q(name__icontains=search) | Q(phone__icontains=search))    
        ser = serializers.BookSerializer(books, many=True)
        return Response(ser.data)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book_setting(request, book_id):
    book = models.BookSetting.objects.get(book__id=book_id)
    ser = serializers.BookSettingSerializer(book)
    return Response(ser.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book_settings(request, court_id):
    book = models.BookSetting.objects.filter(book__court__id=court_id)
    ser = serializers.BookSettingSerializer(book, many=True)
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






