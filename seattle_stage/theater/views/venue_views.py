from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from theater.models import Event, Venue, Company
from theater.forms import VenueForm, CompanyForm
from theater.filters import VenueFilter
import theater.form_helpers as form_helpers
import view_helpers

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



## Venue Index ################################################################
#
#@login_required
def venue_index(request):
  venues = Venue.objects.all()
  venues_filtered = VenueFilter(request.GET, queryset=venues)

  context = {
      'venues': venues_filtered,
      }

  return render(request, 'theater/venue_index.html', context)
#
#
###############################################################################



## Venue Detail ###############################################################
#
#@login_required
def venue_detail(request, venue_pk):
  venue = Venue.objects.get(pk=venue_pk)
  context = {
      'venue': venue,
      }
  return render(request, 'theater/venue_detail.html', context)
#
#
###############################################################################



## New Venue ##################################################################
#
@login_required
def venue_new(request):
  if request.method == 'POST':
    new_venue, form_is_complete, venue_form = form_helpers.modelFromFormPost(
        Venue, VenueForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    venue_form = VenueForm()
  context = {
      'form': venue_form,
      }
  return render(request, 'theater/venue_new.html', context)
#
#
###############################################################################



## Edit Venue #################################################################
#
@login_required
def venue_edit(request, venue_pk):
  venue = Venue.objects.get(pk=venue_pk)
  if request.method == 'POST':
    form_is_complete, venue_form = form_helpers.updateModelFromFormPost(
        venue, VenueForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    venue_form = VenueForm(initial=venue.formInitialData())

  context = {
      'venue_pk': venue_pk,
      'form': venue_form,
      }

  return render(request, 'theater/venue_edit.html', context)
#
#
###############################################################################



## Delete Venue ###############################################################
#
@login_required
def venue_delete(request, venue_pk):
  if request.method == 'POST':
    venue = Venue.objects.get(pk=venue_pk)
    venue.delete()
    return redirect('theater:admin_dashboard')
  return redirect('theater:venue_detail', venue_pk=venue_pk)
#
#
###############################################################################
