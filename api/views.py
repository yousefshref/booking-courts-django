from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from . import serializers
from . import models



todays_date = str(datetime.today())[0:10]


# -------------------------------------------------AUTH-------------------------------------------------------

def create_settings(user_id):
    instance = models.Setting(
        user_id=user_id
    )
    instance.save()

@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = models.CustomUser.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        if user.is_superuser:
            create_settings(user.pk)
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





# -------------------------------------------------USER-------------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = models.CustomUser.objects.get(pk=request.user.pk)
    ser = serializers.UserSerializer(user)
    return Response(ser.data)




# -------------------------------------------------COURT-------------------------------------------------------




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court_types(request):
    states = models.CourtType.objects.all()
    ser = serializers.CourtTypeSerializer(states, many=True)
    return Response(ser.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court_types_2(request):
    states = models.CourtTypeT.objects.all()
    ser = serializers.CourtTypeTSerializer(states, many=True)
    return Response(ser.data)






@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court_videos(request):
  ser = serializers.CourtVideoSerializer(data=request.data)
  if ser.is_valid():
      ser.save()
      return Response(ser.data)
  return Response(ser.errors)
  # return Response({"":""})



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_court_videos(request, video_id):
    video = models.CourtVideo.objects.get(pk=video_id)
    video.delete()
    return Response({"success":True})




@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court_images(request):
    ser = serializers.CourtImageSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_court_images(request, image_id):
    image = models.CourtImage.objects.get(pk=image_id)
    image.delete()
    return Response({"success":True})




@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court_features(request):
    ser = serializers.CourtFeatureSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_court_feature(request, feature_id):
    image = models.CourtFeature.objects.get(pk=feature_id)
    image.delete()
    return Response({"success":True})



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
        create_court_additional(ser.data['id'], request.data.get('tools'))
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_delete(request, court_id):
    court = models.Court.objects.get(pk=court_id)
    court.delete()
    return Response({"success":True})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_courts(request):
    courts = models.Court.objects.all()
    
    if request.user.is_superuser:
      courts = models.Court.objects.filter(Q(user=request.user) | Q(user__staff_for=request.user))

    if request.user.is_staff:
      manager = models.CustomUser.objects.get(id=request.user.staff_for.pk)
      all_staffs = models.CustomUser.objects.filter(staff_for__pk=manager.pk)

      ids = []
      for i in all_staffs.all():
        ids.append(i.pk)
      
      courts = models.Court.objects.filter(Q(user=request.user.staff_for) | Q(user__id__in=ids))


    # price from
    if request.GET.get('price_from'):
       courts = courts.filter(Q(price_per_hour__gte=request.GET.get('price_from')))
    # price to
    if request.GET.get('price_to'):
       courts = courts.filter(Q(price_per_hour__lte=request.GET.get('price_to')))
    # state
    if request.GET.get('state'):
       courts = courts.filter(Q(state__id=request.GET.get('state')))
    # type
    if request.GET.get('type'):
       courts = courts.filter(Q(type__id=request.GET.get('type')))
    # type2
    if request.GET.get('type2'):
       courts = courts.filter(Q(type2__id=request.GET.get('type2')))
    # offers
    if request.GET.get('offer') == 'true':
       courts = courts.filter(Q(offer_price_per_hour__gte=0))
    # events
    if request.GET.get('event') == 'true':
       courts = courts.filter(Q(event=True))


    ser = serializers.CourtSerializer(courts.order_by('-id'), many=True)
    return Response(ser.data)




def generate_hourly_intervals(start_time, end_time):
    # Check if start_time and end_time are datetime objects
    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        raise ValueError("start_time and end_time must be datetime objects.")

    # Check if start_time and end_time are the same
    if start_time == end_time:
        # Define the ending interval
        end_interval = end_time + timedelta(hours=1)

        # Return a single interval that covers the entire hour
        return [f"{start_time.strftime('%H:%M:%S')}-{end_interval.strftime('%H:%M:%S')}"]

    # Initialize an empty array to store the intervals
    intervals = []

    # Define the starting interval
    current_interval_start = start_time.replace(minute=0, second=0, microsecond=0)

    # Define the ending interval
    end_interval = end_time.replace(minute=0, second=0, microsecond=0)

    # Loop through each hour between start_time and end_time (including end_time)
    while current_interval_start <= end_interval:
        # Define the ending interval as the next hour after the current interval
        current_interval_end = current_interval_start + timedelta(hours=1)

        # Append the interval to the array
        intervals.append(f"{current_interval_start.strftime('%H:%M:%S')}-{current_interval_end.strftime('%H:%M:%S')}")

        # Update the current interval
        current_interval_start = current_interval_start + timedelta(hours=1)

    return intervals

def generate_intervals(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%H:%M:%S")

    if start_time == end_time:
        start_time = datetime.strptime("00:00:00", "%H:%M:%S")
        end_time = datetime.strptime("23:59:59", "%H:%M:%S") + timedelta(seconds=1)

    intervals = []
    current_time = start_time
    while current_time < end_time:
        next_time = min(current_time + timedelta(hours=1), end_time)
        intervals.append(f"{current_time.strftime('%H:%M:%S')}-{next_time.strftime('%H:%M:%S')}")
        current_time = next_time

    return intervals


def generate_dates(start_date, end_date, excluded_dates=None):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)[0:10]
        # if excluded_dates is not None or date_str not in excluded_dates:
        dates.append(date_str)
        current_date += timedelta(days=7)
    return dates

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_court(request, court_id):
    court = models.Court.objects.get(pk=court_id)
    court_ser = serializers.CourtSerializer(court)

    # admin
    # all stafs of this admin
    book_times = models.BookTime.objects.filter(Q(book__court__id=court_id)).order_by('-id')

    if request.user.is_superuser:
      all_staffs = models.CustomUser.objects.filter(staff_for=request.user)
      ids=[]
      for i in all_staffs.all():
          ids.append(i.pk)
      book_times.filter(Q(book__court__user=request.user) | Q(book__court__user__id__in=ids))

    if request.user.is_staff:
      admin = models.CustomUser.objects.get(pk=request.user.staff_for.pk)
      all_staffs = models.CustomUser.objects.filter(staff_for=admin)
      ids=[]
      for i in all_staffs.all():
          ids.append(i.pk)
      book_times.filter(Q(book__court__user=admin) | Q(book__court__user__id__in=ids))

    # all pinned times
    todays_date = str(datetime.today())[0:10]
    current_date = datetime.now().date()
    all_pinned_times_for_this_court = []
    for i in book_times:
      if i.book_to_date is not None:
        pinned_times = generate_dates(datetime.strptime(str(todays_date), '%Y-%m-%d'), datetime.strptime(str(i.book_to_date)[0:10], '%Y-%m-%d'))
        for p in pinned_times:
          all_pinned_times_for_this_court.append(p)



    # filter and search

    book_date = request.GET.get('book_date')
    if book_date:
      try:
        book_times = book_times.filter(
          Q(book__book_date=book_date) | (len(all_pinned_times_for_this_court) > 0 and book_date in all_pinned_times_for_this_court and Q(book_to_date__gte=current_date))
        )
        print(book_times)
      except:
        book_times = []


    event = request.GET.get('event')
    if event:
        book_times = book_times.filter(event=event)

    search = request.GET.get('search')
    if search:
        book_times = book_times.filter((Q(book__name__icontains=search) | Q(book__phone__icontains=search)))

    paied_with = request.GET.get('paied_with')
    if paied_with:
        book_times = book_times.filter((Q(paied=paied_with)))

    is_paied = request.GET.get('is_paied')
    if is_paied:
        book_times = book_times.filter((Q(is_paied=is_paied)))

    book_times_ser = serializers.BookTimeSerializer(book_times, many=True)






    # get warning before booking
    court_settings = models.Setting.objects.get(Q(user=court.user) | Q(user=court.user.staff_for))

    if request.user.is_superuser:
      all_staff = models.CustomUser.objects.filter(staff_for=request.user)
      ids = []
      for i in all_staff.all():
          ids.append(i.pk)
      court_settings = models.Setting.objects.get(Q(user=request.user) | Q(user__id__in=ids))

    if request.user.is_staff:
      admin = models.CustomUser.objects.get(pk=request.user.staff_for.pk)
      all_staff = models.CustomUser.objects.filter(staff_for=admin)
      ids = []
      for i in all_staff.all():
          ids.append(i.pk)
      court_settings = models.Setting.objects.get(Q(user=admin) | Q(user__id__in=ids))


    # get numbers can pay later
    numbers = models.Number.objects.filter(setting=court_settings)
    numbers_ser = serializers.NumbergSerializer(numbers, many=True)

    # print(generate_intervals(str(court.open), str(court.close)))

    data = {
        "court":court_ser.data,
        "booked_times":book_times_ser.data,
        # "slots":generate_hourly_intervals(datetime.strptime(str(court.open), "%H:%M:%S"), datetime.strptime(str(court.close), "%H:%M:%S")),
        "slots":generate_intervals(str(court.open), str(court.close)),
        "paying_warning":court_settings.paying_warning,
        "numbers":numbers_ser.data,
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

# def create_book_setting(book_id):
#     book_setting = models.BookSetting(
#         book_id=book_id
#     )
#     book_setting.save()

def create_book_times(book_id, times):
    for i in times:
      instance = models.BookTime(
        book_id=book_id,
        book_from=i['book_from'],
        book_to=i['book_to'],
        book_to_date=i['book_to_date'],
        with_ball=i['with_ball'],
        event=i['event'],
        paied=i['paied'],
        is_paied=i['is_paied'],
        is_cancelled=i['is_cancelled'],
        is_cancelled_day=i['is_cancelled_day'],
      )
      instance.save()
      instance.tools.set(i['tools'])
      instance.save()


import requests

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    data = request.data.copy()
    data['user'] = request.user.pk

    ser = serializers.BookSerializer(data=data)
    if ser.is_valid():
        book = ser.save()
        # create_book_setting(book.id)
        create_book_times(book.id, request.data['book_time'])
        # book
        # book_from
        # book_to
        # book_to_date
        # book_to_date_cancel
        # with_ball
        # event
        # paied
        # is_cancel
        
        # send sms
        court = models.Court.objects.get(id=book.court.pk)
        message = f"تم حجز الملعب {court.title} بأسم {book.name}, يرجي قراءة الشروط واتباعها لتجنب المشاكل تاريخ العملية {str(datetime.today())[0:10]} وتاريخ الحجز {str(book.book_date)}"
        url = f"https://smsmisr.com/api/SMS/?environment=2&username=BE0MFV77&password=c63a781dd862e4d1cb36fe031481a65bf9d1ef5f5df9368e63133e86f34ab175&language=2&sender=527fdd77da70f404ed394f76fd1d44d4ab067a319c2109a8d343ed94a4e099ee&mobile={book.phone}&message={message}"
        headers = {"Content-Type": "application/json"}
        requests.post(url, headers=headers)

        return Response(ser.data)
    return Response(ser.errors)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_books(request):

  # books = models.Book.objects.all()

  # if request.user.is_superuser:
  #   all_stafs = models.CustomUser.objects.filter(staff_for=request.user)
  #   books = books.filter(Q(court__user=request.user) | Q(court__user__id__in=all_stafs))

  # if request.user.is_staff:
  #   all_stafs = models.CustomUser.objects.filter(staff_for=request.user.staff_for)
  #   books = books.filter(Q(court__user=request.user) | Q(court__user__id__in=all_stafs))


  # if not request.user.is_staff and not request.user.is_superuser:
  #   books = books.filter(Q(user=request.user))
     
  # books = books.filter(Q(book_date__gte=datetime.today()))
  # # date
  # if request.GET.get('date_from') and request.GET.get('date_to'):
  #    books = books.filter(Q(book_date__range=[request.GET.get('date_from'), request.GET.get('date_to')]))


  # ser = serializers.BookSerializer(books, many=True)

  
  times = models.BookTime.objects.filter(book__user=request.user)

  if request.GET.get('date_from'):
    times = times.filter(Q(book__book_date__gte=request.GET.get('date_from')) | Q(book_to_date__gte=request.GET.get('date_from')))

  if request.GET.get('date_to'):
    times = times.filter(Q(book__book_date__lte=request.GET.get('date_to')))

  times_ser = serializers.BookTimeSerializer(times, many=True)

  data = {
    # "books":ser.data,
    "times":times_ser.data,
  } 
  
  return Response(data)


def convert_to_days_and_add_to_date(hours, input_date):
  days = int(hours / 24)  # Convert hours to whole days
  new_date = input_date + timedelta(days=days)
  return new_date


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_book(request, book_id):

    if request.user.is_superuser or request.user.is_staff:
      book = models.Book.objects.get(pk=book_id)
    else:
      book = models.Book.objects.get(user=request.user, pk=book_id)

    book_ser = serializers.BookSerializer(book)

    # get if can be deleted
    settings = models.Setting.objects.get(Q(user=book.court.user) | Q(user=book.court.user.staff_for))
    book_created_at = book.created_at
    # days_time
    time_to_cancel = settings.cancel_time_limit
    # limited day
    limited_date = convert_to_days_and_add_to_date(time_to_cancel, book_created_at)
    # compare
    limited_date_formated = datetime.strptime(str(limited_date), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d")
    todays_date = datetime.strptime(str(datetime.today()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")

    can_delete = todays_date <= limited_date_formated
    if request.user.is_superuser or request.user.is_staff:
      can_delete = True

    data = {
       "book":book_ser.data,
       "can_delete":can_delete
    }
    return Response(data)



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

    slots_from = [convert_to_24_hour_format(slot.split('-')[0]) for slot in slots]
    slots_to = [convert_to_24_hour_format(slot.split('-')[1]) for slot in slots]

    court = models.Court.objects.get(id=court_id)
 
    # get booked times
    book_times = []
    
    todays_date = str(datetime.today())[0:10]

    exists = times.filter(
      Q(book_from__in=slots_from) and Q(book_to__in=slots_to) and Q(is_cancelled=False)
    )

    for exist in exists:

      # pinned_time_after_cancel_day = None
      # if exist.book_to_date != None and exist.is_cancelled_day != None:
      #   pinned_time_after_cancel_day = generate_dates(datetime.strptime(str(todays_date), '%Y-%m-%d'), datetime.strptime(str(exist.book_to_date), '%Y-%m-%d'), datetime.strptime(str(exist.is_cancelled_day), '%Y-%m-%d'))

      pinned_time = None
      if exist.book_to_date != None:
        pinned_time = generate_dates(datetime.strptime(str(todays_date), '%Y-%m-%d'), datetime.strptime(str(exist.book_to_date), '%Y-%m-%d'))


      if pinned_time is not None:
        filterd = str(court_date) in pinned_time
        if filterd:
          book_times.append(f"{str(exist.book_from)[0:10]}-{str(exist.book_to)[0:10]}")

      # if pinned_time_after_cancel_day is not None:
      #   filterd = str(court_date) in pinned_time_after_cancel_day
      #   if filterd:
      #     book_times.append(f"{str(exist.book_from)[0:10]}-{str(exist.book_to)[0:10]}")
      
      if str(exist.book.book_date) == str(court_date):
        book_times.append(f"{str(exist.book_from)[0:10]}-{str(exist.book_to)[0:10]}")




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


    for time in selected_times:
      # event
      if court.event == True and event == 'true' and court.event_price != 0 and str(court.event_from)[:5] <= str(time['book_from']) < str(court.event_to)[:5]:
        event_price += court.event_price
        price += court.event_price

      # offer
      if court.offer_price_per_hour is not None and court.offer_price_per_hour != 0 and str(court.offer_from)[:5] <= str(time['book_from']) < str(court.offer_to)[:5]:
        offers_prices += court.offer_price_per_hour
        price += court.offer_price_per_hour
      
      price += court.price_per_hour
        


    checkourt_date = {
        "total_price":price,
        "ball":ball,
        "event_price":event_price,
        "offers_prices":offers_prices,
    }



    # book = models.BookSetting.objects.filter(book__court__id=court_id)
    # ser = serializers.BookSettingsSerializer(book, many=True)

    data = {
        # 'settings':ser.data,
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
        # book_setting = get_object_or_404(models.BookSetting, book__pk=book_id)
        # # Get the existing tool IDs associated with the BookSetting object
        # existing_tool_ids = book_setting.tools.values_list('pk', flat=True)
        # # Get the list of tool IDs received in the request
        # tools_data = request.data.get('tools', [])

        # # Add new tools and remove missing tools
        # for tool_id in tools_data:
        #     if tool_id not in existing_tool_ids:
        #         # Add new tool
        #         book_setting.tools.add(tool_id)
        # for tool_id in existing_tool_ids:
        #     if tool_id not in tools_data:
        #         # Remove missing tool
        #         book_setting.tools.remove(tool_id)




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



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, book_id):
  book = models.Book.objects.get(id=book_id)

  # check if notified
  times = models.BookTime.objects.filter(book__pk=book.pk)

  notifications = models.Notification.objects.filter(Q(book_time__id__in=times) and Q(is_sent=False))

  for notification in notifications:
    # send message
    # court_url = f"http://localhost:3000/courts/{notification.book_time.book.court.pk}"
    court_url = f"https://booking-courts-nextjs-5sei.vercel.app/courts/{notification.book_time.book.court.pk}"
    message = f"الملعب {notification.book_time.book.court.title} فارغ من هذا الوقت {str(notification.slot)} يمكنك حجزة الأن {court_url}"
    url = f"https://smsmisr.com/api/SMS/?environment=2&username=BE0MFV77&password=c63a781dd862e4d1cb36fe031481a65bf9d1ef5f5df9368e63133e86f34ab175&language=2&sender=527fdd77da70f404ed394f76fd1d44d4ab067a319c2109a8d343ed94a4e099ee&mobile={notification.user.phone}&message={message}"
    headers = {"Content-Type": "application/json"}
    requests.post(url, headers=headers)
    notification.is_sent = True
    notification.save()
    

  # book.is_cancelled = True
  # book.save()
  return Response({"success":True})




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time(request, time_id):
  instance = models.BookTime.objects.get(id=time_id)
  try: 
    pinned_times = generate_dates(datetime.strptime(str(todays_date), '%Y-%m-%d'), datetime.strptime(str(instance.book_to_date), '%Y-%m-%d'))
  except:
    pinned_times = []
     
  data = {
    'pinned_times': pinned_times
  }
  return Response(data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time_update(request, time_id):
  instance = models.BookTime.objects.get(id=time_id)
  data = request.data.copy()

  print(request.GET.get('tools'))
  try:
    arr = []
    for i in request.GET.get('tools').split(','):
      arr.append(i)
    instance.tools.set(arr)
  except:
    instance.tools.set([])

  ser = serializers.BookTimeSerializer(instance, data=data, partial=True)
  if ser.is_valid():
    ser.save()
    instance.book.save()
    return Response(ser.data)
  return Response(ser.errors)
  # return Response({"":""})

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time_delete(request, time_id):
  instance = models.BookTime.objects.get(id=time_id)
  instance.delete()
  instance.book.save()
  return Response({"success":True})





@api_view(['GET'])
def get_numbers(request, setting_id):
  try:
    numbers = models.Number.objects.filter(setting__id=setting_id)
    ser = serializers.NumbergSerializer(numbers, many=True)
    return Response(ser.data)
  except:
    return Response({"error":"Not Found"})


@api_view(['DELETE'])
def delete_numbers(request, number_id):
  try:
    numbers = models.Number.objects.filter(id=number_id)
    numbers.delete()
    return Response({"success":True})
  except:
    return Response({"error":"Not Found"})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_number(request):
  ser = serializers.NumbergSerializer(data=request.data)
  if ser.is_valid():
    ser.save()
    return Response(ser.data)
  return Response(ser.errors)
 
   


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_settings(request):

  path = request.GET.get('path')

  # get settings
  settings = models.Setting.objects.all()

  if request.user.is_superuser:
    settings = models.Setting.objects.get(Q(user=request.user))

  if request.user.is_staff:
    all_stafs = models.CustomUser.objects.filter(staff_for=request.user.staff_for)
    settings = models.Setting.objects.get(Q(user=request.user.staff_for) | Q(user__id__in=all_stafs))
  
  ser = serializers.SettingSerializer(settings)



  books = models.Book.objects.all()
  if request.user.is_superuser:
    staffs = models.CustomUser.objects.filter(staff_for=request.user)
    ids=[]
    for i in staffs.all():
       ids.append(i.pk)
    books = books.filter(Q(court__user=request.user) | Q(court__user__id__in=ids))
  
  if request.user.is_staff:
    staffs = models.CustomUser.objects.filter(staff_for=request.user.staff_for)
    ids=[]
    for i in staffs.all():
       ids.append(i.pk)
    books = books.filter(Q(court__user=request.user) | Q(court__user__id__in=ids))

  # display deleted books
  deleted_books = []
  # try:
  #   if settings.paying_time_limit != None and int(settings.paying_time_limit) > 0:
  #     for book in books:
  #       # limited time
  #       limited_time_to_pay = settings.paying_time_limit
  #       # created time
  #       created_book_time = book.created_at
  #       # add limited to created book time
  #       limited_date_to_pay = convert_to_days_and_add_to_date(limited_time_to_pay, created_book_time)
  #       # compare
  #       limited_date_formated = datetime.strptime(str(limited_date_to_pay), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d")
  #       todays_date = datetime.strptime(str(datetime.today()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")

  #       print(limited_date_formated < todays_date and not book.is_paied)

  #       if limited_date_formated < todays_date and not book.is_paied:
  #         #  delete book
  #         if path == '/profile' and (request.user.is_superuser or request.user.is_staff) and book.is_cancelled == False:
  #           deleted_books.append({
  #             "user": book.user.username,
  #             "name": book.name,
  #             "phone": book.phone,
  #             "court": book.court.title,
  #             "created_at": str(book.created_at),
  #             "book_date": str(book.book_date),
  #           })
  #           book.is_cancelled = True
  #           book.save()
  #           settings.save()
  #         settings.save()
  #       settings.save()
  #     settings.save()
  #   settings.save()
  # except:
  #    pass


  # get cancelled books
  # cancelled_books = books.filter(Q(is_cancelled=True))

  if request.GET.get('cancel_from'):
    cancelled_books = cancelled_books.filter(Q(book_date__gte=request.GET.get('cancel_from')))

  if request.GET.get('cancel_to'):
    cancelled_books = cancelled_books.filter(Q(book_date__lte=request.GET.get('cancel_to')))

  if request.GET.get('cancel_search'):
    cancelled_books = cancelled_books.filter(Q(name__icontains=request.GET.get('cancel_search')) | Q(phone__icontains=request.GET.get('cancel_search')))
     
  cancelled_ser = serializers.BookSerializer(cancelled_books, many=True)

  
  data = {
     "settings":ser.data,
     "deleted_books":deleted_books,
     "cancelled_books":cancelled_ser.data,
  }
  return Response(data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_settings(request):

  if request.user.is_superuser:
    settings = models.Setting.objects.get(user=request.user)

  if request.user.is_staff:
    settings = models.Setting.objects.get(user=request.user.staff_for)

  ser = serializers.SettingSerializer(settings, data=request.data, partial=True)
  if ser.is_valid():
      ser.save()
      return Response(ser.data)
  return Response(ser.errors)
  











@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_staff(request):
    if request.user.is_superuser:
      ser = serializers.UserSerializer(data=request.data)
      if ser.is_valid():
          ser.save()
          return Response(ser.data)
      return Response(ser.errors)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_staffs(request):
    if request.user.is_superuser:
      staffs = models.CustomUser.objects.filter(staff_for__pk=request.user.pk)
      ser = serializers.UserSerializer(staffs, many=True)
      return Response(ser.data)









# staffs permissions
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def staff_details(request, staff_id):
  if request.user.is_superuser:
    # get his information
    staff = models.CustomUser.objects.get(pk=staff_id)
    staff_ser = serializers.UserSerializer(staff)

    # get his courts
    staff_courts = models.Court.objects.filter(user=staff)
    court_ser = serializers.CourtSerializer(staff_courts, many=True)

    # get his books - with total pricing
    staff_books = models.Book.objects.filter(user=staff)

    if request.GET.get('date_from') and request.GET.get('date_to'):
       staff_books = staff_books.filter(book_date__range=[request.GET.get('date_from'), request.GET.get('date_to')])

    book_ser = serializers.BookSerializer(staff_books, many=True)

    books_total_earning_paied = 0
    books_total_earning_not_paied = 0

    for i in staff_books.all():
      if i.is_paied:
         books_total_earning_paied += i.total_price

      if not i.is_paied:
         books_total_earning_not_paied += i.total_price


    data = {
       "staff_details":staff_ser.data,
       "staff_courts":court_ser.data,
       "staff_books":book_ser.data,
       "staff_books_summerize":{
          "total_paied":books_total_earning_paied,
          "total_not_paied":books_total_earning_not_paied,
       },
    }      

    return Response({"data":data})
  return Response({"error":"redirect"})




# {'user': 12, 'court': '86', 'slot': '9:00PM-10:00PM'}
# create notifiation
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_notification(request):
  data = request.data.copy()
  data['user'] = request.user.pk

  times = models.BookTime.objects.filter(Q(book__court__pk=data['court']))
  slot1 = convert_to_24_hour_format(data['slot'][0:7])
  slot2 = convert_to_24_hour_format(data['slot'][8:16])

  book_time = None
  for time in times.all():
    if str(time.book_from) == str(slot1) and str(time.book_to) == str(slot2):
      book_time = time.pk
  
  data['book_time'] = book_time

  ser = serializers.NotificationSerializer(data=data)
  if ser.is_valid():
    ser.save()
    return Response(ser.data)
  return Response(ser.errors)







