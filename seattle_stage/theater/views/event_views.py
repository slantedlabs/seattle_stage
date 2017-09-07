from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404
import datetime
from dateutil.relativedelta import relativedelta

from theater.models import Event, Venue, Company
from theater.forms import EventForm
from theater.filters import EventFilter
import view_helpers
import theater.form_helpers as form_helpers


## TODO:
#
#  Date/Times
#    * filtering dashboard (on venue, company, time window, price?,
#      neighborhood, classification, etc.)
#    * month view, week view, day view
#
#  Company view
#    * people, description
#    * recent/upcoming shows they've done
#
#  Venue view
#    * Google maps, info, link to venue website
#    * recent/upcoming shows there



## Events Index View ##########################################################
#
#@login_required
def event_index(request):
  events = Event.objects.all()
  context = {
      'events': events,
      }
  return render(request, 'theater/event_index.html', context)
#
#
###############################################################################



## Events Detail View #########################################################
#
#@login_required
def event_detail(request, event_pk):
  event = Event.objects.get(pk=event_pk)
  context = {
      'event': event,
      }
  return render(request, 'theater/event_detail.html', context)
#
#
###############################################################################



## Month Calendar View ########################################################
#
#@login_required
def event_month(request):
  today = timezone.now()

  mutable_GET = request.GET.copy()

  view_date = datetime.datetime.strptime(mutable_GET.get('date',
    today.strftime('%m/%Y')), '%m/%Y')
  print(view_date)

  if mutable_GET.get('date', None) is None:
    mutable_GET.update({'date': today.strftime('%m/%Y')})
  
  next_month = view_date + relativedelta(months=+1)
  last_month = view_date + relativedelta(months=-1)

  events = Event.objects.all()
  events_filtered = EventFilter(mutable_GET, queryset=events)

  context = {
      'events': events_filtered,
      'year': view_date.year,
      'month': view_date.month,
      'next_month': next_month.strftime('%m/%Y'),
      'last_month': last_month.strftime('%m/%Y'),
      'this_month': today.strftime('%m/%Y'),
      'get_params': mutable_GET,
      }

  return render(request, 'theater/month.html', context)
#
#
###############################################################################



## AJAX Update Month Calendar View ############################################
#
#@login_required
def ajax_update_event_month(request):
  try:
    view_date = datetime.datetime.strptime(request.GET.get('date', ''),
        '%m/%Y')
  except ValueError as e:
    print(e)
    raise Http404
  else:
    print(view_date)

  today = timezone.now()
  next_month = view_date + relativedelta(months=+1)
  last_month = view_date + relativedelta(months=-1)

  events = Event.objects.all()
  events_filtered = EventFilter(request.GET, queryset=events)

  context = {
      'events': events_filtered.qs,
      'year': view_date.year,
      'month': view_date.month,
      'next_month': next_month.strftime('%m/%Y'),
      'last_month': last_month.strftime('%m/%Y'),
      'this_month': today.strftime('%m/%Y'),
      }

  return render(request, 'theater/frags/month_calendar.html', context)
#
#
###############################################################################



## Week Calendar View #########################################################
#
#@login_required
def event_week(request):
  today = timezone.now()

  mutable_GET = request.GET.copy()

  view_date = datetime.datetime.strptime(mutable_GET.get('date',
    today.strftime('%m/%d/%Y')), '%m/%d/%Y')

  view_week = view_helpers.weekNum(view_date)

  if mutable_GET.get('date', None) is None:
    mutable_GET.update({'date': today.strftime('%m/%d/%Y')})
  
  if view_date.day < (view_helpers.weekdaySundayZero(view_date) + 1):
    last_week_adj = view_date.day
  else:
    last_week_adj = view_helpers.weekdaySundayZero(view_date) + 1

  daysleft_month = view_helpers.daysInMonth(view_date) - view_date.day
  daysleft_week = 6 - view_helpers.weekdaySundayZero(view_date)
  if daysleft_month < daysleft_week:
    next_week_adj = daysleft_month + 1
  else:
    next_week_adj = 7 - view_helpers.weekdaySundayZero(view_date)

  next_week = view_date + relativedelta(days=+next_week_adj)
  last_week = view_date + relativedelta(days=-last_week_adj)

  events = Event.objects.all()
  events_filtered = EventFilter(mutable_GET, queryset=events)

  context = {
      'events': events_filtered,
      'year': view_date.year,
      'month': view_date.month,
      'week': view_week,
      'next_week': next_week.strftime('%m/%d/%Y'),
      'last_week': last_week.strftime('%m/%d/%Y'),
      'get_params': mutable_GET,
      }

  return render(request, 'theater/week.html', context)
#
#
###############################################################################



## Day List View ##############################################################
#
#  This provides a list of all the Event objects that are happening on the
#  given date (year, month, day).
#
#@login_required
def event_day(request):
  today = timezone.now()

  mutable_GET = request.GET.copy()
  if mutable_GET.get('year', None) is None:
    mutable_GET.update({'year': today.year})
  if mutable_GET.get('month', None) is None:
    mutable_GET.update({'month': today.month})
  if mutable_GET.get('day', None) is None:
    mutable_GET.update({'day': today.day})
  
  year = mutable_GET.get('year', today.year)
  month = mutable_GET.get('month', today.month)
  day = mutable_GET.get('day', today.day)

  view_date = datetime.date(int(year), int(month), int(day))

  yesterday = view_date + relativedelta(days=-1)
  tomorrow = view_date + relativedelta(days=+1)

  events = Event.objects.all()
  events_filtered = EventFilter(mutable_GET, queryset=events)

  context = {
      'events': events_filtered,
      'year': year,
      'month': month,
      'day': day,
      'tomorrow': tomorrow,
      'yesterday': yesterday,
      'get_params': mutable_GET,
      }

  return render(request, 'theater/day.html', context)
#
#
###############################################################################



## Event New ##################################################################
#
@login_required
def event_new(request):
  if request.method == 'POST':
    new_event, form_is_complete, event_form = form_helpers.modelFromFormPost(
        Event, EventForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    event_form = EventForm()
  context = {
      'form': event_form,
      }
  return render(request, 'theater/event_new.html', context)
#
#
###############################################################################



## Event Edit #################################################################
#
@login_required
def event_edit(request, event_pk):
  event = Event.objects.get(pk=event_pk)
  if request.method == 'POST':
    form_is_complete, event_form = form_helpers.updateModelFromFormPost(
        event, EventForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    event_form = EventForm(initial=event.formInitialData())

  context = {
      'event_pk': event_pk,
      'form': event_form,
      }

  return render(request, 'theater/event_edit.html', context)
#
#
###############################################################################



## Event Delete ###############################################################
#
@login_required
def event_delete(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.get(pk=event_pk)
    event.delete()
    return redirect('theater:admin_dashboard')
  return redirect('theater:event_detail', event_pk=event_pk)
#
#
###############################################################################
