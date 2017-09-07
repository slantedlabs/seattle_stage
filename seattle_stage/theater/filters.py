from django import forms

from .models import Venue, Company, Event

# Stupid hack because on NetBSD django_filters installs as just filters
try:
  import django_filters
except ImportError as e:
  try:
    import filters as django_filters
  except ImportError as e:
    raise ImportError("No modules name django_filters or filters")


class VenueFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains',
      label="Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
  description = django_filters.CharFilter(name='description',
      lookup_expr='icontains',
      label="Keywords",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))

  class Meta:
    model = Venue
    fields = ['name',]



class CompanyFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains',
      label="Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
  classification = django_filters.ChoiceFilter(name='classification',
      label="Type",
      label_suffix='',
      choices=Company.CLASSIFICATION_CHOICES,
      widget=forms.Select(attrs={'class': 'form-control'}))
  description = django_filters.CharFilter(name='description',
      lookup_expr='icontains',
      label="Keywords",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))

  class Meta:
    model = Company
    fields = ['name', 'brief_name', 'classification',]



class EventFilter(django_filters.FilterSet):
  TICKET_PRICES = [
      (5, "$5"),
      (10, "$10"),
      (25, "$25"),
      (50, "$50"),
      (100, "$100"),
      ]

  SHOW_LENGTHS = [
      (1, "1 hour"),
      (2, "2 hours"),
      ]

  START_TIMES = [
      (3, "3:00 pm"),
      (5, "5:00 pm"),
      (7, "7:00 pm"),
      (9, "9:00 pm"),
      ]

  name = django_filters.CharFilter(lookup_expr='icontains',
      label="Title",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))
  description = django_filters.CharFilter(name='description',
      lookup_expr='icontains',
      label="Keywords",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': 'form-control'}))

  ticket_price__lt = django_filters.ChoiceFilter(name='ticket_price',
      lookup_expr='lt',
      label="Price",
      label_suffix='',
      choices=TICKET_PRICES,
      widget=forms.Select(attrs={'class': 'form-control'}))
  show_length__lt = django_filters.ChoiceFilter(name='show_length',
      lookup_expr='lt',
      label="Length",
      label_suffix='',
      choices=SHOW_LENGTHS,
      widget=forms.Select(attrs={'class': 'form-control'}))

  date = django_filters.DateTimeFilter(name='date_and_time',
      lookup_expr='gte',
      label="Date",
      label_suffix='',
      input_formats=[
        '%m/%Y',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y',
        ],
      widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))

  starts_after = django_filters.ChoiceFilter(name='date_and_time',
      lookup_expr='hour__gte',
      label="Starts after",
      label_suffix='',
      choices=START_TIMES,
      widget=forms.Select(attrs={'class': 'form-control'}))

  company_type = django_filters.ChoiceFilter(name='company',
      lookup_expr='classification',
      label="Company type",
      label_suffix='',
      choices=Company.CLASSIFICATION_CHOICES,
      widget=forms.Select(attrs={'class': 'form-control'}))

  company = django_filters.ModelChoiceFilter(queryset=Company.objects.all(),
      name='company',
      label="Company",
      label_suffix='',
      widget=forms.Select(attrs={'class': "form-control"}))
  
  venue = django_filters.ModelChoiceFilter(queryset=Venue.objects.all(),
      name='venue',
      label="Venue",
      label_suffix='',
      widget=forms.Select(attrs={'class': "form-control"}))

  class Meta:
    model = Event
    fields = ['name', 'venue', 'company',]
