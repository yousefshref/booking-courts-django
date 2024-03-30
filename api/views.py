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
from rest_framework import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


todays_date = str(datetime.today())[0:10]
todays_date_not_str = datetime.today()

# functions
def get_hours_between(start_time, end_time):
  """
  This function takes two times in the format "HH:MM:SS" and returns a list of hours between them.

  Args:
      start_time: The start time in the format "HH:MM:SS".
      end_time: The end time in the format "HH:MM:SS".

  Returns:
      A list of hours between the start and end time, inclusive.
  """
  start_datetime = datetime.strptime(start_time, "%H:%M:%S")
  end_datetime = datetime.strptime(end_time, "%H:%M:%S")

  # Handle the case where the start time is after the end time
  if start_datetime > end_datetime:
    end_datetime = end_datetime + timedelta(days=1)

  hours = []
  current_time = start_datetime
  while current_time <= end_datetime:
    hours.append(current_time.strftime("%H"))
    current_time += timedelta(hours=1)

  return hours

def generate_dates(start_date, end_date, excluded_dates=None):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)[0:10]
        # if excluded_dates is not None or date_str not in excluded_dates:
        dates.append(date_str)
        current_date += timedelta(days=7)
    return dates
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



# password reset
class PasswordResetRequestView(APIView):
  def post(self, request):
      serializer = serializers.PasswordResetRequestSerializer(data=request.data)
      if serializer.is_valid():
          email = serializer.validated_data['email']
          user = models.CustomUser.objects.get(email=email)
          uid = urlsafe_base64_encode(force_bytes(user.pk))
          token = default_token_generator.make_token(user)
          reset_url = f"{settings.FRONTEND_URL}auth/password-reset/{uid}/{token}/"

          # Email configuration
          sender_email = "yb2005at@gmail.com"
          receiver_email = email
          password = "qxqy rckl ywtc ckmd"

          # Create a multipart message
          message = MIMEMultipart()
          message["From"] = sender_email
          message["To"] = receiver_email
          message["Subject"] = "LinkawyX Password Reset."

          # Add body to email
          body = f"Follow this link to reset your account password {reset_url}"
          message.attach(MIMEText(body, "plain"))

          # Establish a secure connection with the SMTP server
          server = smtplib.SMTP("smtp.gmail.com", 587)
          server.starttls()

          # Login to the email server
          server.login(sender_email, password)

          # Send the email
          server.sendmail(sender_email, receiver_email, message.as_string())

          # Quit the server
          server.quit()
          return Response(status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = models.CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


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
  # exist->edit | not->create
  data = request.data.copy()


  if data['is_free'] == 'true' or data['is_free'] == True:
    data['is_free'] = True
  else:
    data['is_free'] = False

  if data['is_available'] == 'true' or data['is_available'] == True:
    data['is_available'] = True
  else:
    data['is_available'] = False


  try:
    exist = models.CourtFeature.objects.get(id=data.get('id'))
    exist.feature = data['feature']
    exist.is_available = data['is_available']
    exist.is_free = data['is_free']
    exist.save()
    return Response({"updated":"true"})
  except:
    new_insance = models.CourtFeature(
       court_id=data['court'],
       feature=data['feature'],
       is_free=data['is_free'],
       is_available=data['is_available'],
    )
    new_insance.save()
    return Response({"created":"true"})
  # return Response({"":""})


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_court_feature(request, feature_id):
    image = models.CourtFeature.objects.get(pk=feature_id)
    image.delete()
    return Response({"success":True})



# {
# "court":88,
# "feature":"test",
# "is_free":"False",
# "is_available":"True"
# }
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court_tools(request):
    data = request.data.copy()
    additional = models.CourtAdditional.objects.get(court__id=data['court'])
    data['court_additional'] = additional.pk

    # if with id->edit | NOT->create

    try:
      exist = models.CourtAdditionalTool.objects.get(pk=data.get('id'))
      exist.title = data['title']
      exist.price = data['price']
      exist.save()
      return Response({"updated":"true"})
    except:
      # create
      court_additional = models.CourtAdditional.objects.get(court__id=data['court'])
      new_instace = models.CourtAdditionalTool(
        court_additional=court_additional,
        title=data['title'],
        price=data['price'],
      )
      new_instace.save()
      return Response({"created":"true"})


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_court_tool(request, court_id):
    image = models.CourtAdditionalTool.objects.get(pk=court_id)
    image.delete()
    return Response({"success":True})



      
def create_court_additional(court_id):
    court_additional = models.CourtAdditional(
        court_id=court_id,
    )
    court_additional.save()


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_court(request):
    ser = serializers.CourtSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        create_court_additional(ser.data['id'])
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
def get_admin_times(request):
  all_staff = None
  if request.user.is_superuser:
    all_staff = models.CustomUser.objects.filter(Q(staff_for=request.user.pk))
  else:
    all_staff = models.CustomUser.objects.filter(Q(staff_for=request.user.staff_for.pk))

  ids = []
  for i in all_staff:
    ids.append(i.pk)
     
  times = models.BookTime.objects.filter(
    Q(book__court__user=request.user)
    | Q(book__court__user=request.user.staff_for) | Q(book__court__user__id__in=ids)
  )

  # name phone
  if request.GET.get('search'):
    times = times.filter(Q(book__name__icontains=request.GET.get('search')) | Q(book__phone__icontains=request.GET.get('search')))
  
  # cancelled
  if request.GET.get('is_cancelled'):
    times = times.filter(Q(is_cancelled=request.GET.get('is_cancelled')))

  # date
  if request.GET.get('from'):
    times = times.filter(Q(book__book_date__gte=request.GET.get('from')))
  if request.GET.get('to'):
    times = times.filter(Q(book__book_date__lte=request.GET.get('to')))
     

  ser = serializers.BookTimeSerializer(times, many=True)

  return Response(ser.data)




# -------------------------------------------------------BOOK----------------------------------------------------





@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_books(request, court_id):
  times = models.BookTime.objects.filter(
     Q(book__court__id=court_id) and (Q(book__court__user=request.user) or Q(book__court__user=request.user.staff_for))
  )

  search = request.GET.get('search')
  if search:
    times = times.filter(Q(book__name__icontains=search) | Q(book__phone__icontains=search))
    
  all_pinned_times_for_this_court = []
  for i in times:
    if i.book_to_date is not None:
      pinned_times = generate_dates(datetime.strptime(str(i.book.book_date), '%Y-%m-%d'), datetime.strptime(str(i.book_to_date)[0:10], '%Y-%m-%d'))
      for p in pinned_times:
        all_pinned_times_for_this_court.append(p)
        
  book_date = request.GET.get('book_date')
  if book_date and len(all_pinned_times_for_this_court) > 0 and book_date in all_pinned_times_for_this_court:
    times = times.filter(
      Q(book_to_date__gte=book_date) 
      | 
      Q(book__book_date=book_date)
    )
  elif book_date:
    times = times.filter(Q(book__book_date=book_date))
  
  is_cancelled = request.GET.get('is_cancelled')
  if is_cancelled:
    times = times.filter(
      Q(is_cancelled=True)
    )
  
  is_paied = request.GET.get('is_paied')
  if is_paied:
    times = times.filter(
      Q(is_paied=True)
    )

  paied = request.GET.get('paied')
  if paied:
    times = times.filter(
      Q(paied=paied)
    )

  ser = serializers.BookTimeSerializer(times, many=True)
  return Response(ser.data)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_courts(request):
    courts = models.Court.objects.all()
    
    if request.user.is_superuser:
      courts = courts.filter(Q(user=request.user) | Q(user__staff_for=request.user))

    if request.user.is_staff:
      manager = models.CustomUser.objects.get(id=request.user.staff_for.pk)
      all_staffs = models.CustomUser.objects.filter(staff_for__pk=manager.pk)

      ids = []
      for i in all_staffs.all():
        ids.append(i.pk)
      
      courts = courts.filter(Q(user=request.user.staff_for) | Q(user__id__in=ids))


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


    # latest courts
    latest_courts = models.Court.objects.all().order_by('-id')[:5]
    latest_courts_ser = serializers.CourtSerializer(latest_courts, many=True)

    data = {
       "courts": ser.data,
       'lates_courts': latest_courts_ser.data
    }

    return Response(data)




def generate_intervals(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%H:%M:%S")
    interval_delta = timedelta(minutes=60)

    # If start time equals end time, set end time to one day later
    if start_time == end_time:
        end_time += timedelta(days=1)

    intervals = []
    current_time = start_time
    while current_time < end_time:
        next_time = min(current_time + interval_delta, end_time)
        intervals.append(f"{current_time.strftime('%H:%M:%S')}-{next_time.strftime('%H:%M:%S')}")
        current_time = next_time

    return intervals


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_court(request, court_id):
    court = models.Court.objects.filter(pk=court_id)

    # get warning before booking
    court_settings = models.Setting.objects.get(Q(user=court.first().user) | Q(user=court.first().user.staff_for))


    if request.user.is_superuser:
      all_staff = models.CustomUser.objects.filter(staff_for=request.user)
      ids = []
      for i in all_staff.all():
          ids.append(i.pk)
      court = court.get(Q(user=request.user) | Q(user__id__in=ids))
      court_settings = models.Setting.objects.get(Q(user=request.user) | Q(user__id__in=ids))

    if request.user.is_staff:
      admin = models.CustomUser.objects.get(pk=request.user.staff_for.pk)
      all_staff = models.CustomUser.objects.filter(staff_for=admin)
      ids = []
      for i in all_staff.all():
          ids.append(i.pk)
      court = court.get(Q(user=admin) | Q(user__id__in=ids))
      court_settings = models.Setting.objects.get(Q(user=admin) | Q(user__id__in=ids))

    court_settings_ser = serializers.SettingSerializer(court_settings)
    
    data = {}
    try:
      court_ser_admin = serializers.CourtSerializer(court)
      data = {
          "court":court_ser_admin.data,
          "slots":generate_intervals(str(court.open), str(court.close)),
          "paying_warning":court_settings.paying_warning,
          "court_settings":court_settings_ser.data,
      }
    except:
      court_ser = serializers.CourtSerializer(court.first())
      data = {
          "court":court_ser.data,
          "slots":generate_intervals(str(court.first().open), str(court.first().close)),
          "paying_warning":court_settings.paying_warning,
          "court_settings":court_settings_ser.data,
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
        # update_additional_tools(ser.data['id'], request.data['tools'])
        return Response(ser.data)
    return Response(ser.errors)



# -------------------------------------------------BOOK-------------------------------------------------------



def create_book_times(book_id, times):
    for i in times:
      if i['with_ball'] == 'true':
        i['with_ball'] = True
      else:
        i['with_ball'] = False

      if i['event'] == 'true':
        i['event'] = True
      else:
        i['event'] = False

      if i['is_paied'] == 'true':
        i['is_paied'] = True
      else:
        i['is_paied'] = False

      if i['is_cancelled'] == 'true':
        i['is_cancelled'] = True
      else:
        i['is_cancelled'] = False

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
        create_book_times(book.id, request.data['book_time'])
        # send sms
        court = models.Court.objects.get(id=book.court.pk)
        message = f"تم حجز الملعب {court.title} بأسم {book.name}, يرجي قراءة الشروط واتباعها لتجنب المشاكل تاريخ العملية {str(datetime.today())[0:10]} وتاريخ الحجز {str(book.book_date)}"
        url = f"https://smsmisr.com/api/SMS/?environment=1&username=BE0MFV77&password=c63a781dd862e4d1cb36fe031481a65bf9d1ef5f5df9368e63133e86f34ab175&language=2&sender=527fdd77da70f404ed394f76fd1d44d4ab067a319c2109a8d343ed94a4e099ee&mobile={book.phone}&message={message}"
        headers = {"Content-Type": "application/json"}
        requests.post(url, headers=headers, proxies={'http':'','https':''})

        return Response(ser.data)
    return Response(ser.errors)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_books(request):
  
  times = models.BookTime.objects.filter(book__user=request.user)

  if request.GET.get('date_from'):
    times = times.filter(Q(book__book_date__gte=request.GET.get('date_from')) | Q(book_to_date__gte=request.GET.get('date_from')))

  if request.GET.get('date_to'):
    times = times.filter(Q(book__book_date__lte=request.GET.get('date_to')))

  times_ser = serializers.BookTimeSerializer(times, many=True)

  data = {
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

    data = {
       "book":book_ser.data,
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
    
    exists = times.filter(
      Q(book_from__in=slots_from) and Q(book_to__in=slots_to) and Q(is_cancelled=False)
    )

    for exist in exists:

      # pinned_time_after_cancel_day = None
      # if exist.book_to_date != None and exist.is_cancelled_day != None:
      #   pinned_time_after_cancel_day = generate_dates(datetime.strptime(str(todays_date), '%Y-%m-%d'), datetime.strptime(str(exist.book_to_date), '%Y-%m-%d'), datetime.strptime(str(exist.is_cancelled_day), '%Y-%m-%d'))

      pinned_time = None
      if exist.book_to_date != None:
        pinned_time = generate_dates(datetime.strptime(str(exist.book.book_date), '%Y-%m-%d'), datetime.strptime(str(exist.book_to_date), '%Y-%m-%d'))


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

    data = {
        'booked':book_times,
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
        return Response(ser.data)
    return Response(ser.errors)







@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_over_time(request):
  ser = serializers.OverTimeSerializer(data=request.data)
  if ser.is_valid():
    ser.save()
    return Response(ser.data)
  return Response(ser.errors)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_over_time(request, over_time_id):
  instance = models.OverTime.objects.get(id=over_time_id)
  instance.delete()
  return Response({"success":True})





@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time(request, time_id):
  instance = models.BookTime.objects.get(id=time_id)
  try: 
    pinned_times = generate_dates(datetime.strptime(str(instance.book.book_date), '%Y-%m-%d'), datetime.strptime(str(instance.book_to_date), '%Y-%m-%d'))
  except:
    pinned_times = []
  
  # can deleted
  # settings
  if instance.book.court.user.is_staff:
    settings = models.Setting.objects.get(user=instance.book.court.user.staff_for)
  else:
    settings = models.Setting.objects.get(user=instance.book.court.user)

  book_created_at = instance.book.created_at
  # days_time
  can_delete = False
  time_to_cancel = settings.cancel_time_limit
  if time_to_cancel > 0:
    # limited day
    limited_date = convert_to_days_and_add_to_date(time_to_cancel, book_created_at)
    # compare
    limited_date_formated = datetime.strptime(str(limited_date), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d")
    todays_date = datetime.strptime(str(datetime.today()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")

    can_delete = todays_date <= limited_date_formated and not instance.is_paid

  if request.user.is_superuser:
    can_delete = True
  
  data = {
    'pinned_times': pinned_times,
    'can_delete': can_delete,
  }
  return Response(data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time_update(request, time_id):
  instance = models.BookTime.objects.get(id=time_id)
  data = request.data.copy()
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
    instance.save()

    # send sms
    if instance.is_cancelled:
      notifications = models.Notification.objects.filter(Q(book_time__id=instance.pk) and Q(is_sent=False))

      for notification in notifications:
        # court_url = f"http://localhost:3000/courts/{notification.book_time.book.court.pk}"
        court_url = f"https://sports.linkawyx.com/courts/{notification.book_time.book.court.pk}"
        message = f"الملعب {notification.book_time.book.court.title} فارغ من هذا الوقت {str(notification.slot)} يمكنك حجزة الأن {court_url}"
        url = f"https://smsmisr.com/api/SMS/?environment=1&username=BE0MFV77&password=c63a781dd862e4d1cb36fe031481a65bf9d1ef5f5df9368e63133e86f34ab175&language=2&sender=527fdd77da70f404ed394f76fd1d44d4ab067a319c2109a8d343ed94a4e099ee&mobile={notification.user.phone}&message={message}"
        headers = {"Content-Type": "application/json"}
        requests.post(url, headers=headers, proxies={'http':'','https':''})
        notification.is_sent = True
        notification.save()

    # settings
    if instance.book.court.user.is_staff:
      settings = models.Setting.objects.get(user=instance.book.court.user.staff_for)
      settings.save()
    else:
      settings = models.Setting.objects.get(user=instance.book.court.user)
      settings.save()

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
    ser = serializers.NumbergSerializer(numbers.order_by('-id'), many=True)
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
  data = request.data.copy()
  user = models.CustomUser.objects.get(phone=data['number'])
  data['user'] = user.pk
  ser = serializers.NumbergSerializer(data=data)
  if ser.is_valid():
    ser.save()
    return Response(ser.data)
  return Response(ser.errors)
 
   


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_settings(request):
  # get settings
  settings = models.Setting.objects.all()

  if request.user.is_superuser:
    settings = models.Setting.objects.get(Q(user=request.user))

  if request.user.is_staff:
    all_stafs = models.CustomUser.objects.filter(staff_for=request.user.staff_for)
    settings = models.Setting.objects.get(Q(user=request.user.staff_for) | Q(user__id__in=all_stafs))
  
  ser = serializers.SettingSerializer(settings)

  books = models.BookTime.objects.all()
  if request.user.is_superuser:
    staffs = models.CustomUser.objects.filter(staff_for=request.user)
    ids=[]
    for i in staffs.all():
       ids.append(i.pk)
    books = books.filter(Q(book__court__user=request.user) | Q(book__court__user__id__in=ids))
  
  if request.user.is_staff:
    staffs = models.CustomUser.objects.filter(staff_for=request.user.staff_for)
    ids=[]
    for i in staffs.all():
       ids.append(i.pk)
    books = books.filter(Q(book__court__user=request.user) | Q(book__court__user__id__in=ids))


  # display deleted books when i open profile in ui
  deleted_books = []
  try:
    all_times = models.BookTime.objects.filter(is_cancelled=False, is_paied=False)

    numbers = models.Number.objects.filter(setting__id=settings.pk)
    numbers_arr = []
    for i in numbers:
      numbers_arr.append(i.number)

    for time in all_times:
      if time.book.user.phone not in numbers_arr and time.book.created_at > convert_to_days_and_add_to_date(settings.paying_time_limit, time.book.created_at):
        deleted_books.append({
          "book":{
              "name":time.book.name,
              "phone":time.book.phone,
              "date":str(time.book.book_date),
          },
          "court":{
              "title":time.book.court.title,
          },
        })
        time.is_cancelled = True
        time.is_paied = False
        time.save()
      settings.save()
  except:
     pass


  # get cancelled books
  cancelled_books = books.filter(Q(is_cancelled=True))

  if request.GET.get('cancel_from'):
    cancelled_books = cancelled_books.filter(Q(book__book_date__gte=request.GET.get('cancel_from')))

  if request.GET.get('cancel_to'):
    cancelled_books = cancelled_books.filter(Q(book__book_date__lte=request.GET.get('cancel_to')))

  if request.GET.get('cancel_search'):
    cancelled_books = cancelled_books.filter(Q(book__name__icontains=request.GET.get('cancel_search')) | Q(book__phone__icontains=request.GET.get('cancel_search')))
     
  cancelled_ser = serializers.BookTimeSerializer(cancelled_books, many=True)

  
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

from django.db.models import Sum

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_staffs(request):
  if request.user.is_superuser:
    staffs = models.CustomUser.objects.filter(staff_for__pk=request.user.pk).order_by('-id')
    staff_details = []
    for s in staffs:
      courts = models.Court.objects.filter(Q(user__pk=s.pk)).order_by('-id')

      books = models.BookTime.objects.filter(Q(book__user__pk=s.pk)).order_by('-id')
      books__ = models.BookTime.objects.filter(Q(book__user__pk=s.pk)).order_by('-id')
      
      
      if request.GET.get('date_from') and request.GET.get('date_to'):
        books__ = books__.filter(book__book_date__range=[request.GET.get('date_from'), request.GET.get('date_to')])
        books = books.filter(book__book_date__range=[request.GET.get('date_from'), request.GET.get('date_to')])
      
      b_ser = serializers.BookTimeSerializer(books, many=True)
      c_ser = serializers.CourtSerializer(courts, many=True)

      b_success = books__.filter(Q(is_paied=True))
      b_waiting = books__.filter(Q(is_paied=False) & Q(is_cancelled=False))
      b_faild = books__.filter(Q(is_cancelled=True))

      books_money_details = {
         "success":b_success.aggregate(total_sum=Sum('total_price'))['total_sum'],
         "waiting":b_waiting.aggregate(total_sum=Sum('total_price'))['total_sum'],
         "faild":b_faild.aggregate(total_sum=Sum('total_price'))['total_sum'],
      }
      staff_details.append({
        "name":s.username,
        "email":s.email,
        "courts":c_ser.data,
        "books":b_ser.data,
        "moneyDetails":books_money_details
      })

    return Response(staff_details)








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
  slot1 = convert_to_24_hour_format(data['slot'].split('-')[1])
  slot2 = convert_to_24_hour_format(data['slot'].split('-')[0])

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







