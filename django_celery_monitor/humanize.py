"""Some helpers to humanize values."""
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from django.utils.translation import gettext as _
from django.utils.timezone import now


def pluralize_year(n):
    """Return a string with the number of years ago."""
    return _(f'{n} year ago') if n == 1 else _(f'{n} years ago')


def pluralize_month(n):
    """Return a string with the number of months ago."""
    return _(f'{n} month ago') if n == 1 else _(f'{n} months ago')


def pluralize_week(n):
    """Return a string with the number of weeks ago."""
    return _(f'{n} week ago') if n == 1 else _(f'{n} weeks ago')


def pluralize_day(n):
    """Return a string with the number of days ago."""
    return _(f'{n} day ago') if n == 1 else _(f'{n} days ago')


OLDER_CHUNKS = (
    (365.0, pluralize_year),
    (30.0, pluralize_month),
    (7.0, pluralize_week),
    (1.0, pluralize_day),
)


def naturaldate(date, include_seconds=False):
    """Convert datetime into a human natural date string."""
    if not date:
        return ''

    right_now = now()
    today = datetime(right_now.year, right_now.month,
                     right_now.day, tzinfo=right_now.tzinfo)
    delta = right_now - date
    delta_midnight = today - date

    days = delta.days
    hours = delta.seconds // 3600
    minutes = delta.seconds // 60
    seconds = delta.seconds

    if days < 0:
        return _('just now')

    if days == 0:
        if hours == 0:
            if minutes > 0:
                return _(f'{minutes} minute ago') if minutes == 1 else _(f'{minutes} minutes ago')
            else:
                if include_seconds and seconds:
                    return _(f'{seconds} second ago') if seconds == 1 else _(f'{seconds} seconds ago')
                return _('just now')
        else:
            return _(f'{hours} hour ago') if hours == 1 else _(f'{hours} hours ago')

    if delta_midnight.days == 0:
        return _('yesterday at {time}').format(time=date.strftime('%H:%M'))

    count = 0
    for chunk, pluralizefun in OLDER_CHUNKS:
        if days >= chunk:
            count = int(round((delta_midnight.days + 1) / chunk, 0))
            fmt = pluralizefun(count)
            return fmt.format(num=count)
