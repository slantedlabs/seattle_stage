from __future__ import unicode_literals

from django.db import models


## Venue Model ################################################################
#
#  This model contains all the information about a pysical location that will
#  actually host shows.
#
#  TODO: photo
#
class Venue(models.Model):
  name = models.CharField(max_length=200, unique=True)
  brief_name = models.CharField(max_length=200, null=True)
  description = models.TextField(null=True)
  website_url = models.URLField(null=True)
  image = models.ImageField(upload_to='venue_images/', null=True)

  # Venue Address
  street_address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  state = models.CharField(max_length=200, null=True)
  zip_code = models.IntegerField(null=True)

  def __unicode__(self):
    return self.name

  def hasAddress(self):
    return (self.street_address and self.city and self.state)

  def address(self):
    address = ""
    if self.street_address and self.city and self.state and self.zip_code:
      address = "{} {}, {} {}".format(self.street_address, self.city,
          self.state, self.zip_code)
    return address

  def addressQuery(self):
    request_address = '+'.join(self.street_address.split())
    request_city = '+'.join(self.city.split())
    request_city_state = '+'.join([request_city] + self.state.split())
    return ','.join([request_address, request_city_state])

  def slug(self):
    return '_'.join(self.name.split())

  def formInitialData(self):
    initial_data = {
        'name': self.name,
        'brief_name': self.brief_name,
        'description': self.description,
        'website_url': self.website_url,
        'street_address': self.street_address,
        'city': self.city,
        'state': self.state,
        'zip_code': self.zip_code,
        }
    return initial_data

  def updateFromValidForm(self, validated_form):
    self.name = validated_form.cleaned_data['name']
    self.brief_name = validated_form.cleaned_data['brief_name']
    self.description = validated_form.cleaned_data['description']
    self.website_url = validated_form.cleaned_data['website_url']
    self.street_address = validated_form.cleaned_data['street_address']
    self.city = validated_form.cleaned_data['city']
    self.state = validated_form.cleaned_data['state']
    self.zip_code = validated_form.cleaned_data['zip_code']
    self.save()

  @classmethod
  def fromValidForm(cls, validated_form):
    new_venue = cls(name=validated_form.cleaned_data['name'],
        brief_name=validated_form.cleaned_data['brief_name'],
        description=validated_form.cleaned_data['description'],
        website_url=validated_form.cleaned_data['website_url'],
        street_address=validated_form.cleaned_data['street_address'],
        city=validated_form.cleaned_data['city'],
        state=validated_form.cleaned_data['state'],
        zip_code=validated_form.cleaned_data['zip_code'])
    new_venue.save()
    return new_venue
#
#
###############################################################################



## Company Model ##############################################################
#
#  This model contains all of the necessary info about a group that puts on
#  shows.
#
#  TODO: photo
#
class Company(models.Model):
  FRINGE = "Fringe"
  PROFESSIONAL = "Professional"
  EDUCATIONAL = "Educational"
  CLASSIFICATION_CHOICES = [
      (FRINGE, "Fringe"),
      (PROFESSIONAL, "Professional"),
      (EDUCATIONAL, "Educational"),
      ]

  name = models.CharField(max_length=200, unique=True)
  brief_name = models.CharField(max_length=200, null=True)
  description = models.TextField(null=True)
  website_url = models.URLField(null=True)
  classification = models.CharField(max_length=200, null=True)
  image = models.ImageField(upload_to='company_images/', null=True)

  def __unicode__(self):
    return self.name

  def slug(self):
    return '_'.join(self.name.split())

  def formInitialData(self):
    initial_data = {
        'name': self.name,
        'brief_name': self.brief_name,
        'description': self.description,
        'website_url': self.website_url,
        'classification': self.classification,
        }
    return initial_data

  def updateFromValidForm(self, validated_form):
    self.name = validated_form.cleaned_data['name']
    self.brief_name = validated_form.cleaned_data['brief_name']
    self.description = validated_form.cleaned_data['description']
    self.website_url = validated_form.cleaned_data['website_url']
    self.classification = validated_form.cleaned_data['classification']
    self.save()

  @classmethod
  def fromValidForm(cls, validated_form):
    new_company = cls(name=validated_form.cleaned_data['name'],
        brief_name=validated_form.cleaned_data['brief_name'],
        description=validated_form.cleaned_data['description'],
        website_url=validated_form.cleaned_data['website_url'],
        classification=validated_form.cleaned_data['classification'])
    new_company.save()
    return new_company
#
#
###############################################################################



## Event Model ################################################################
#
#  This model contains all the info about a specific event -- when it's
#  happening, the Venue it's at, how much it costs, which Group is putting it
#  on, etc.
#
#  TODO: photo
#
class Event(models.Model):
  name = models.CharField(max_length=200)
  date_and_time = models.DateTimeField()

  brief_name = models.CharField(max_length=200, null=True)
  description = models.TextField(null=True)
  blurb = models.TextField(null=True)
  website_url = models.URLField(null=True)
  ticket_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
  ticket_url = models.URLField(null=True)
  show_length = models.IntegerField(null=True)
  image = models.ImageField(upload_to='event_images/', null=True)
  featured = models.BooleanField(default=False)

  venue = models.ForeignKey(Venue)
  company = models.ForeignKey(Company)

  def __unicode__(self):
    if self.company:
      return "{} by {}".format(self.name, self.company.name)
    else:
      return self.name

  def slug(self):
    return '_'.join(self.name.split())

  def formInitialData(self):
    initial_data = {
        'name': self.name,
        'date_and_time': self.date_and_time.strftime("%m/%d/%Y %H:%M %p"),
        'brief_name': self.brief_name,
        'description': self.description,
        'blurb': self.blurb,
        'website_url': self.website_url,
        'ticket_price': self.ticket_price,
        'ticket_url': self.ticket_url,
        'show_length': self.show_length,
        'venue': self.venue,
        'company': self.company,
        'image': self.image,
        'featured': self.featured,
        }
    return initial_data

  def updateFromValidForm(self, validated_form):
    self.name = validated_form.cleaned_data['name']
    self.date_and_time = validated_form.cleaned_data['date_and_time']
    self.brief_name = validated_form.cleaned_data['brief_name']
    self.description = validated_form.cleaned_data['description']
    self.blurb = validated_form.cleaned_data['blurb']
    self.website_url = validated_form.cleaned_data['website_url']
    self.ticket_price = validated_form.cleaned_data['ticket_price']
    self.ticket_url = validated_form.cleaned_data['ticket_url']
    self.show_length = validated_form.cleaned_data['show_length']
    self.venue = validated_form.cleaned_data['venue']
    self.company = validated_form.cleaned_data['company']
    self.image = validated_form.cleaned_data['image']
    self.featured = validated_form.cleaned_data['featured']
    self.save()

  @classmethod
  def fromValidForm(cls, validated_form):
    new_company = cls(name = validated_form.cleaned_data['name'],
        date_and_time = validated_form.cleaned_data['date_and_time'],
        brief_name = validated_form.cleaned_data['brief_name'],
        description = validated_form.cleaned_data['description'],
        blurb = validated_form.cleaned_data['blurb'],
        website_url = validated_form.cleaned_data['website_url'],
        ticket_price = validated_form.cleaned_data['ticket_price'],
        ticket_url = validated_form.cleaned_data['ticket_url'],
        show_length = validated_form.cleaned_data['show_length'],
        venue = validated_form.cleaned_data['venue'],
        company = validated_form.cleaned_data['company'],
        image = validated_form.cleaned_data['image'],
        featured = validated_form.cleaned_data['featured'])
    new_company.save()
    return new_company
#
#
###############################################################################
