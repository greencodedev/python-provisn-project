from datetime import datetime, timedelta
from calendar import HTMLCalendar

import pytz

USE_TZ = False

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):

		amsterdam = pytz.timezone('Europe/Amsterdam')
		events_per_day = events.filter(date_of_event__day=day)
		d = ''
		for event in events_per_day:
			d += f' {event.get_html_url}'

		if day != 0:
			return f"<td style='vertical-align: initial;'><span class='date'>{day}</span>{d} </td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		from userdashboard.models import BlockchainEvent
		events = BlockchainEvent.objects.filter(date_of_event__year=self.year, date_of_event__month=self.month)
		#events = Event.objects.all()

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
