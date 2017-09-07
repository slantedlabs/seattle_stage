from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from theater.models import Event, Venue, Company
from theater.forms import CompanyForm, VenueForm
from theater.filters import CompanyFilter
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



## Company Index ##############################################################
#
#@login_required
def company_index(request):
  companies = Company.objects.all()
  companies_filtered = CompanyFilter(request.GET, queryset=companies)
  context = {
      'companies': companies_filtered,
      }
  return render(request, 'theater/company_index.html', context)
#
#
###############################################################################



## Company Detail #############################################################
#
#@login_required
def company_detail(request, company_pk):
  company = Company.objects.get(pk=company_pk)
  context = {
      'company': company,
      }
  return render(request, 'theater/company_detail.html', context)
#
#
###############################################################################



## New Company ##################################################################
#
@login_required
def company_new(request):
  if request.method == 'POST':
    new_company, form_is_complete, company_form = form_helpers.modelFromFormPost(
        Company, CompanyForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    company_form = CompanyForm()
  context = {
      'form': company_form,
      }
  return render(request, 'theater/company_new.html', context)
#
#
###############################################################################



## Edit Company #################################################################
#
@login_required
def company_edit(request, company_pk):
  company = Company.objects.get(pk=company_pk)
  if request.method == 'POST':
    form_is_complete, company_form = form_helpers.updateModelFromFormPost(
        company, CompanyForm, request)
    if form_is_complete:
      return redirect('theater:admin_dashboard')
  else:
    company_form = CompanyForm(initial=company.formInitialData())

  context = {
      'company_pk': company_pk,
      'form': company_form,
      }

  return render(request, 'theater/company_edit.html', context)
#
#
###############################################################################



## Delete Company ###############################################################
#
@login_required
def company_delete(request, company_pk):
  if request.method == 'POST':
    company = Company.objects.get(pk=company_pk)
    company.delete()
    return redirect('theater:admin_dashboard')
  return redirect('theater:company_detail', company_pk=company_pk)
#
#
###############################################################################
