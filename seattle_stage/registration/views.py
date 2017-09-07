from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from theater.models import Venue, Company, Event
from theater.forms import VenueForm, CompanyForm, EventForm

import view_helpers

@login_required
def admin_home(request):
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

  return render(request, 'registration/admin_dashboard.html', context)

@login_required
def profile(request):
  return redirect('root_index')

@login_required
def email_change(request):
  if request.method == 'POST':
    request.user.email = request.POST['new_email']
    request.user.save()
    return redirect('root_index')
  return render(request, 'registration/email_change.html')

@login_required
def password_change_done(request):
  return redirect('root_index')
