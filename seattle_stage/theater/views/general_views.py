from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

import view_helpers
from theater.models import Venue, Company, Event
from theater.forms import VenueForm, CompanyForm, EventForm
from theater.filters import EventFilter

#@login_required
def index(request):
  today = timezone.now()
  week = view_helpers.weekNum(today)
  events = Event.objects.all()
  filtration = {
          'date': today.strftime('%m/%Y'),
          'featured': True,
          }
  events_filtered = EventFilter(filtration, queryset=events)
  context = {
      'today': today,
      'week': week,
      'events': events_filtered.qs,
      }
  return render(request, 'theater/index.html', context)

#@login_required
def suggestions(request):
  events = Event.objects.filter(featured=True)
  context = {
      'features': events,
      }
  return render(request, 'theater/suggestions.html', context)

#@login_required
def scene(request):
  return render(request, 'theater/scene.html')

@login_required
def admin_dashboard(request):
  venues = Venue.objects.all()
  companies = Company.objects.all()
  events = Event.objects.all()

  venue_form_pairs = [
      view_helpers.objectFormPair(v, VenueForm) for v in venues ]
  company_form_pairs = [
      view_helpers.objectFormPair(c, CompanyForm) for c in companies ]
  event_form_pairs = [
      view_helpers.objectFormPair(e, EventForm) for e in events ]

  context = {
      'venue_form_pairs': venue_form_pairs,
      'company_form_pairs': company_form_pairs,
      'event_form_pairs': event_form_pairs,
      }

  return render(request, 'theater/admin_dashboard.html', context)
