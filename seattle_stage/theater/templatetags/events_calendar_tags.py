from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby

from django.urls import reverse

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_events_week_calendar(parser, token):
  """
  The template tag's syntax is {% events_calendar year month week events %}
  """
  try:
    tag_name, year, month, week, events = token.split_contents()
  except ValueError:
    msg = "{} tag requires four arguments".format(token.contents.split()[0])
    raise template.TemplateSyntaxError(msg)
  return EventsWeekCalendarNode(year, month, week, events)


def do_events_month_calendar(parser, token):
  """
  The template tag's syntax is {% events_calendar year month events %}
  """
  try:
    tag_name, year, month, events = token.split_contents()
  except ValueError:
    msg = "{} tag requires three arguments".format(token.contents.split()[0])
    raise template.TemplateSyntaxError(msg)
  return EventsMonthCalendarNode(year, month, events)


class EventsWeekCalendarNode(template.Node):
  """
  Process a particular node in a template. Fail silently.
  """
  def __init__(self, year, month, week, events):
    try:
      self.year = template.Variable(year)
      self.month = template.Variable(month)
      self.week = template.Variable(week)
      self.events = template.Variable(events)
    except ValueError:
      raise template.TemplateSyntaxError

  def render(self, context):
    try:
      # Get the variables from the context so the method is thread-safe.
      my_events = self.events.resolve(context)
      my_year = self.year.resolve(context)
      my_month = self.month.resolve(context)
      my_week = self.week.resolve(context)
      cal = EventsCalendar(my_events)
      return cal.formatoneweek(my_year, my_month, my_week)
    except ValueError:
      return      
    except template.VariableDoesNotExist:
      return


class EventsMonthCalendarNode(template.Node):
  """
  Process a particular node in a template. Fail silently.
  """
  def __init__(self, year, month, events):
    try:
      self.year = template.Variable(year)
      self.month = template.Variable(month)
      self.events = template.Variable(events)
    except ValueError:
      raise template.TemplateSyntaxError

  def render(self, context):
    try:
      # Get the variables from the context so the method is thread-safe.
      my_events = self.events.resolve(context)
      my_year = self.year.resolve(context)
      my_month = self.month.resolve(context)
      cal = EventsCalendar(my_events)
      return cal.formatmonth(int(my_year), int(my_month))
    except ValueError:
      return      
    except template.VariableDoesNotExist:
      return


class EventsCalendar(HTMLCalendar):
  """
  Overload Python's calendar.HTMLCalendar to add the appropriate events to each
  day's table cell.
  """
  def __init__(self, events):
    super(EventsCalendar,self).__init__(6)
    self.events = self.group_by_day(events)

  def formatday(self, day, weekday):
    if day != 0:
      cssclass = self.cssclasses[weekday]
      if date.today() == date(self.year, self.month, day):
        cssclass += ' today'
      body = ["<div class=\"day-contents\">"]
      if day in self.events:
        cssclass += ' filled'
        for event in self.events[day]:
          body.append("<a class=\"no-color\" href=\"{}\">".format(
            reverse("theater:event_detail",
                kwargs={'event_pk': event.pk})))
          body.append("<div class=\"day-event\">")
          body.append("{}".format(event))
          body.append("</div>")
          body.append("</a>")
      body.append("</div>")
      return self.day_cell(cssclass,
          '<span class="daynumber noevent">{}</span> {}'.format(day, ''.join(body)))
    return self.day_cell('noday', '&nbsp;') 

  def formatoneweek(self, year, month, week):
    self.year, self.month = year, month
    v = []
    a = v.append
    a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
    a('\n')
    a(super(EventsCalendar, self).formatweekheader())
    a('\n')
    theweek = super(EventsCalendar, self).monthdays2calendar(year, month)[week]
    a(super(EventsCalendar, self).formatweek(theweek))
    a('\n')
    a('</table>')
    a('\n')
    return ''.join(v)

  def formatmonth(self, year, month):
    self.year, self.month = year, month
    return super(EventsCalendar, self).formatmonth(year, month)

  def group_by_day(self, events):
    field = lambda event: event.date_and_time.day
    return dict(
      [(day, list(items)) for day, items in groupby(events, field)]
    )

  def day_cell(self, cssclass, body):
    return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to templates
register.tag("events_week_calendar", do_events_week_calendar)
register.tag("events_month_calendar", do_events_month_calendar)

