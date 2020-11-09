from django.template.defaultfilters import register

@register.filter
def lookup(d, key):
    return d[key]