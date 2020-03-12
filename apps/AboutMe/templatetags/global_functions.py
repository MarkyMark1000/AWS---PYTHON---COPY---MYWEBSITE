from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    # Apparently, add has side effects, so use this:
    # https://stackoverflow.com/questions/4386168/how-to-concatenate-strings-in-django-templates
    return str(arg1) + str(arg2)

@register.filter
def linkValid(title, href):
    # Ensure title and href have a value for the link to be valid.
    if (title is None) or (href is None):
        return False
    else:
        if len(title)<1 or len(href)<1:
            return False
        else:
            return True