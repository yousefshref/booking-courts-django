from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import F, Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from datetime import datetime, timedelta
from . import serializers
from . import models


# -------------------------------------------------AUTH-------------------------------------------------------

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



# -------------------------------------------------STATE-------------------------------------------------------



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_states(request):
    states = models.State.objects.all()
    ser = serializers.StateSerializer(states, many=True)
    return Response(ser.data)



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_state(request):
    ser = serializers.StateSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_state(request, state_id):
    instance = models.State.objects.get(id=state_id)
    instance.delete()
    return Response({"success":True})



@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_state(request, state_id):
    instance = models.State.objects.get(id=state_id)
    ser = serializers.StateSerializer(instance, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)






# -------------------------------------------------USER-------------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = models.CustomUser.objects.get(pk=request.user.pk)
    ser = serializers.UserSerializer(user)
    return Response(ser.data)




# -------------------------------------------------COURT-------------------------------------------------------


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_type(request):
    ser = serializers.CourtTypeSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_type(request, type_id):
    instance = models.CourtType.objects.get(id=type_id)
    instance.delete()
    return Response({"success":True})



@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_type(request, type_id):
    instance = models.CourtType.objects.get(id=type_id)
    ser = serializers.CourtTypeSerializer(instance, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)





@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court_types(request):
    states = models.CourtType.objects.all()
    ser = serializers.CourtTypeSerializer(states, many=True)
    return Response(ser.data)



def create_additional_tools(additional_id, tools):
    tools_loaded = json.loads(tools)
    for i in tools_loaded:
        tool = models.CourtAdditionalTool(
          court_additional_id=additional_id,
          title=i['title'],
          price=i['price'],
        )
        tool.save()
    
def create_court_additional(court_id, tools):
    court_additional = models.CourtAdditional(
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
        create_court_additional(ser.data['id'], request.data['tools'])
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_courts(request):
    courts = models.Court.objects.all()
    ser = serializers.CourtSerializer(courts, many=True)
    return Response(ser.data)



def generate_hourly_intervals(start_time, end_time):
    # Check if start_time and end_time are datetime objects
    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        raise ValueError("start_time and end_time must be datetime objects.")

    # Initialize an empty array to store the intervals
    intervals = []

    # Define the starting interval
    current_interval_start = start_time.replace(minute=0, second=0, microsecond=0)

    # Define the ending interval
    end_interval = end_time.replace(minute=0, second=0, microsecond=0)

    # Loop through each hour between start_time and end_time
    while current_interval_start < end_interval:
        # Define the ending interval as the next hour after the current interval
        current_interval_end = current_interval_start + timedelta(hours=1)

        # Append the interval to the array
        intervals.append(f"{current_interval_start.strftime('%H:%M:%S')}-{current_interval_end.strftime('%H:%M:%S')}")

        # Update the current interval
        current_interval_start = current_interval_end

    return intervals

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court(request, court_id):
    court = models.Court.objects.get(pk=court_id)
    court_ser = serializers.CourtSerializer(court)

    # get booked times of this court
    current_date = datetime.now().date()
    books = models.BookTime.objects.filter(
    Q(book__court__id=court_id) &
    (Q(book__book_date=current_date) | Q(book_to_date__gte=current_date))
)
    books_ser = serializers.BookTimeSerializer(books, many=True)

    data = {
        "court":court_ser.data,
        "booked_times":books_ser.data,
        "slots":generate_hourly_intervals(datetime.strptime(str(court.open), "%H:%M:%S"), datetime.strptime(str(court.close), "%H:%M:%S"))
    }
    return Response(data)


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
def court_update(request, court_id):
    court = models.Court.objects.get(id=court_id)
    ser = serializers.CourtSerializer(court, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        update_additional_tools(ser.data['id'], request.data['tools'])
        return Response(ser.data)
    return Response(ser.errors)



# -------------------------------------------------BOOK-------------------------------------------------------

def create_book_setting(book_id):
    book_setting = models.BookSetting(
        book_id=book_id
    )
    book_setting.save()

def create_book_times(book_id, times):
    for i in times:
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
    data = request.data.copy()
    data['user'] = request.user.pk

    ser = serializers.BookSerializer(data=data)
    if ser.is_valid():
        book = ser.save()
        create_book_setting(book.id)
        create_book_times(book.id, request.data['book_time'])
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_books(request):
    books = models.Book.objects.filter(user=request.user)
    ser = serializers.BookSerializer(books, many=True)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_book(request, book_id):

    if request.user.is_superuser:
      book = models.Book.objects.get(pk=book_id)
    else:
      book = models.Book.objects.get(user=request.user, pk=book_id)
        
    book_ser = serializers.BookSerializer(book)
    return Response(book_ser.data,)



def convert_to_24_hour_format(time_str):
    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, '%I:%M%p')

    # Extract the hour and minute from the datetime object
    hour = time_obj.hour
    minute = time_obj.minute

    # Return the hour and minute as a string in 24-hour format
    return f"{hour:02d}:{minute:02d}:00"

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_while_booking(request, court_id):
    court_date = request.GET.get('court_date')
    slots = request.GET.get('slots').split(',') #should be 4AM-5AM, 5AM-6AM ...
    times = models.BookTime.objects.filter(book__court__id=court_id)

    court = models.Court.objects.get(id=court_id)
 
    # get booked times
    book_times = []

    for slot in slots:
      for time in times:
        slot1 = convert_to_24_hour_format(slot.split('-')[0])
        slot2 = convert_to_24_hour_format(slot.split('-')[1])
        time1 = time.book_from
        time2 = time.book_to

        f_condition = slot1 == str(time1) and slot2 == str(time2) and str(time.book.book_date) == court_date and str(time.book_to) > str(datetime.now().time())[:5]
        s_condition = time.book_to_date != None and str(time.book_to_date) >= court_date and slot1 == str(time1) and slot2 == str(time2)
        t_condition = time.book_to_date != None and str(time.book.book_date) == court_date and str(time.book_to_date) >= court_date and slot1 == str(time1) and slot2 == str(time2)
        fourth_condition = time.book_to_date == None and str(time.book.book_date) == court_date and slot1 == str(time1) and slot2 == str(time2) and str(time.book_to) > str(datetime.now().time())[:5]
        

        if f_condition or s_condition or t_condition or fourth_condition:
          book_times.append(f"{slot1}-{slot2}")





    # get closed times
    closed_times = []

    for slot in slots:
        slot1 = convert_to_24_hour_format(slot.split('-')[0])
        slot2 = convert_to_24_hour_format(slot.split('-')[1])
        if court.closed_from and str(court.closed_from)[:5] <= slot1 < str(court.closed_to)[:5]:
            closed_times.append(f"{slot1}-{slot2}")






    # get book summerize
    with_ball = request.GET.get('with_ball')
    event = request.GET.get('event')
    selected_times = json.loads(request.GET.get('selected_times'))
    
    ball = 0
    event_price = 0
    offers_prices = 0
    price = 0

    if with_ball == 'true' and court.with_ball:
        ball += court.ball_price * len(selected_times)
        price += court.ball_price * len(selected_times)

    if event == 'true' and court.event:
        event_price += court.event_price * len(selected_times)
        price += court.event_price * len(selected_times)

    for time in selected_times:
        # offer
        if court.offer_price_per_hour is not None and court.offer_price_per_hour != 0 and str(court.offer_from)[:5] <= str(time['book_from']) < str(court.offer_to)[:5]:
          offers_prices += court.offer_price_per_hour
          price += court.offer_price_per_hour
        else:
          price += court.price_per_hour

    checkourt_date = {
        "total_price":price,
        "ball":ball,
        "event_price":event_price,
        "offers_prices":offers_prices,
    }




    book = models.BookSetting.objects.filter(book__court__id=court_id)
    ser = serializers.BookSettingsSerializer(book, many=True)

    data = {
        'settings':ser.data,
        'booked':book_times,
        'price_date':checkourt_date,
        'closed_times':closed_times,
    }
    return Response(data)



@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_update(request, book_id):
    book = models.Book.objects.get(pk=book_id)
    ser = serializers.BookSerializer(book, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        
        # update times and add new time
        times = request.data.get('times', [])
        for time in times:
          time_id = time.get('id')
          book_from = time.get('book_from')
          book_to = time.get('book_to')
          book_to_date = time.get('book_to_date')
          book_to_date_cancel = time.get('book_to_date_cancel')

          if time_id:
              # Check if the time_id exists in the database
              try:
                  book_time = models.BookTime.objects.get(id=time_id, book__id=book_id)
                  # Update the existing instance
                  book_time.book_from = book_from
                  book_time.book_to = book_to
                  book_time.book_to_date = book_to_date
                  book_time.book_to_date_cancel = book_to_date_cancel
                  book_time.save()
              except models.BookTime.DoesNotExist:
                  # If the time_id does not exist, create a new instance
                  models.BookTime.objects.create(
                      book_id=book_id,
                      book_from=book_from,
                      book_to=book_to,
                      book_to_date=book_to_date_cancel,
                      book_to_date_cancel=book_to_date_cancel,
                  )
          else:
              # Create a new instance
              models.BookTime.objects.create(
                  book_id=book_id,
                  book_from=book_from,
                  book_to=book_to,
                  book_to_date=book_to_date
              )






        # update tools and add new tools
        book_setting = get_object_or_404(models.BookSetting, book__pk=book_id)
        # Get the existing tool IDs associated with the BookSetting object
        existing_tool_ids = book_setting.tools.values_list('pk', flat=True)
        # Get the list of tool IDs received in the request
        tools_data = request.data.get('tools', [])

        # Add new tools and remove missing tools
        for tool_id in tools_data:
            if tool_id not in existing_tool_ids:
                # Add new tool
                book_setting.tools.add(tool_id)
        for tool_id in existing_tool_ids:
            if tool_id not in tools_data:
                # Remove missing tool
                book_setting.tools.remove(tool_id)




        # create over time
        try:
          over_time_data = request.data.get('over_time')
          over_time_id = over_time_data.get('id', None)
          
          if over_time_id:
              over_time_instance = get_object_or_404(models.OverTime, pk=over_time_id)
          else:
              over_time_instance = None

          if over_time_instance:
              over_time_instance.book_from = over_time_data.get('book_from', over_time_instance.book_from)
              over_time_instance.book_to = over_time_data.get('book_to', over_time_instance.book_to)
              over_time_instance.note = over_time_data.get('note', over_time_instance.note)
              over_time_instance.price = over_time_data.get('price', over_time_instance.price)
              # over_time_instance.updated_at = timezone.now()
              over_time_instance.save()
          else:
              over_time_instance = models.OverTime.objects.create(
                  book_id=book_id,
                  book_from=over_time_data.get('book_from'),
                  book_to=over_time_data.get('book_to'),
                  note=over_time_data.get('note'),
                  price=over_time_data.get('price'),
              )
        except:
            pass

        return Response(ser.data)
    return Response(ser.errors)

