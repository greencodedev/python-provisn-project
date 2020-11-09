
# -*- coding: utf-8 -*-
"""
Daily cleanup job.
Can be run as a cronjob to clean out old data from the database (only expired
sessions at the moment).
"""
import six

from django.conf import settings
from django.core.cache import caches

from django_extensions.management.jobs import MinutelyJob


class Job(MinutelyJob):
    help = "Updates Currency Prices for Crypto Payments"

    def execute(self):
        ...
