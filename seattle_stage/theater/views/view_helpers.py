from django.utils import timezone
import datetime

from theater.models import Event, Venue, Company


def filter_events(year, month,
    day=None, venue_pk=None, company_pk=None, timewindow_start=None,
    timewindow_end=None, max_price=None, classification=None):

  year = int(year)
  month = int(month)

  if day:
    day = int(day)
    date = datetime.date(year, month, day)
    print(date.strftime("Searching for events on %B %d, %Y."))
    events = Event.objects.filter(date_and_time__year=date.year,
        date_and_time__month=date.month, date_and_time__day=date.day)
  else:
    date = datetime.date(year, month, 1)
    print(date.strftime("Searching for events in %B, %Y."))
    events = Event.objects.filter(date_and_time__year=date.year,
        date_and_time__month=date.month)

  print("Found {}.".format(', '.join([str(e) for e in events])))

  # Filter on Venue
  if venue_pk:
    venue = Venue.objects.get(pk=venue_pk)
    events = events.filter(venue=venue)

  # Filter on Company
  if company_pk:
    company = Company.objects.get(pk=company_pk)
    events = events.filter(company=company)

  # Filter on timewindow
  if timewindow_start:
    start_time = timezone(year, month, day, timewindow_start)
    events = events.filter(date_and_time__gte=start_time)
  if timewindow_end:
    end_time = timezone(year, month, day, timewindow_end)
    events = events.filter(date_and_time__lte=end_time)

  # Filter on price
  if max_price:
    events = events.filter(ticket_price__lte=int(max_price))

  # Filter on company classification
  if classification:
    events = events.filter(company__classification=classification)

  return events



def returnPostToAdmin(request):
  go_to_admin = False
  if request.method == 'POST':
    if request.POST.get('from_admin', None) == 'true':
      go_to_admin = True
  return go_to_admin




## Object Form Pair
#
#  Takes an object with a .formInitialData() member function and returns a
#  pair of that object and a form object of the type FormClass as initialized
#  with the object's initial form data.
#
def objectFormPair(obj, FormClass):
  return (obj, FormClass(obj.formInitialData()))





def weekdaySundayZero(date):
  return (date.weekday() + 1) % 7

def weekNum(date):
  day = date.day
  first = datetime.date(year=date.year, month=date.month, day=1)
  return (weekdaySundayZero(first) - 1 + day) / 7

def daysInMonth(date):
  monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  monthdays_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if (date.year % 4 == 0 and not \
      (date.year % 100 == 0 and not date.year % 400 == 0)):
    num = monthdays_leap[date.month - 1]
  else:
    num = monthdays[date.month - 1]
  return num
