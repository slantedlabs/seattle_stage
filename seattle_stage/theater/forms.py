from django import forms

from .models import Venue, Company


class VenueForm(forms.Form):
  name = forms.CharField(max_length=200,
      label="Venue Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}))
  brief_name = forms.CharField(max_length=200,
      label="Brief Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  website_url = forms.URLField(label="Venue Website",
      label_suffix='',
      widget=forms.URLInput(attrs={'class': "form-control"}),
      required=False)
  street_address = forms.CharField(max_length=200,
      label="Street Address",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  city = forms.CharField(max_length=200,
      label="City",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  state = forms.CharField(max_length=200,
      label="State",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  zip_code = forms.IntegerField(label="Zip Code",
      label_suffix='',
      widget=forms.NumberInput(attrs={'class': "form-control"}),
      required=False)
  image = forms.ImageField(label="Picture",
      label_suffix='',
      widget=forms.ClearableFileInput(attrs={'class': "form-control"}),
      required=False)
  description = forms.CharField(max_length=10000,
      label="Description",
      label_suffix='',
      widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': 15,
        }),
      required=False)




class CompanyForm(forms.Form):
  name = forms.CharField(max_length=200,
      label="Company Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}))
  brief_name = forms.CharField(max_length=200,
      label="Brief Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  website_url = forms.URLField(label="Company Website",
      label_suffix='',
      widget=forms.URLInput(attrs={'class': "form-control"}),
      required=False)
  classification = forms.ChoiceField(label="Classification",
      label_suffix='',
      widget=forms.Select(attrs={'class': "form-control"}),
      choices=Company.CLASSIFICATION_CHOICES,
      required=False)
  image = forms.ImageField(label="Picture",
      label_suffix='',
      widget=forms.ClearableFileInput(attrs={'class': "form-control"}),
      required=False)
  description = forms.CharField(max_length=10000,
      label="Description",
      label_suffix='',
      widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': 15,
        }),
      required=False)



class EventForm(forms.Form):
  name = forms.CharField(max_length=200,
      label="Event Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}))
  brief_name = forms.CharField(max_length=200,
      label="Brief Name",
      label_suffix='',
      widget=forms.TextInput(attrs={'class': "form-control"}),
      required=False)
  date_and_time = forms.DateTimeField(label="Date/Time",
      label_suffix='',
      input_formats=[
        '%m/%d/%Y %H:%M %p',    # '02/15/2017 10:00 AM'
        '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
        '%Y-%m-%d',             # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
        '%m/%d/%Y',             # '10/25/2006'
        '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M',       # '10/25/06 14:30'
        '%m/%d/%y'],            # '10/25/06'
      widget=forms.DateTimeInput(attrs={'class': "form-control datepicker"}))
  website_url = forms.URLField(label="Event Website",
      label_suffix='',
      widget=forms.URLInput(attrs={'class': "form-control"}),
      required=False)
  ticket_price = forms.DecimalField(label="Ticket Price",
      label_suffix='',
      widget=forms.NumberInput(attrs={'class': "form-control"}),
      max_digits=7,
      decimal_places=2,
      required=False)
  ticket_url = forms.URLField(label="Ticketing Website",
      label_suffix='',
      widget=forms.URLInput(attrs={'class': "form-control"}),
      required=False)
  show_length = forms.IntegerField(label="Show Length",
      label_suffix='',
      widget=forms.NumberInput(attrs={'class': "form-control"}),
      required=False)
  venue = forms.ModelChoiceField(queryset=Venue.objects.all(),
      label="Venue",
      label_suffix='',
      widget=forms.Select(attrs={'class': "form-control"}),
      required=False)
  company = forms.ModelChoiceField(queryset=Company.objects.all(),
      label="Company",
      label_suffix='',
      widget=forms.Select(attrs={'class': "form-control"}),
      required=False)
  image = forms.ImageField(label="Picture",
      label_suffix='',
      widget=forms.ClearableFileInput(attrs={'class': "form-control"}),
      required=False)
  blurb = forms.CharField(max_length=10000,
      label="Blurb",
      label_suffix='',
      widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': 5,
        }),
      required=False)
  featured = forms.BooleanField(
      label="Featured",
      label_suffix='',
      widget=forms.CheckboxInput(attrs={
        'class': "form-control"
        }),
      required=False)
  description = forms.CharField(max_length=10000,
      label="Description",
      label_suffix='',
      widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': 15,
        }),
      required=False)

