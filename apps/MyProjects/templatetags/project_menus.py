from apps.MyProjects.models import ProjectLanguage
from django import template

register = template.Library()

# simple tag to make the TrainingGroup menu accessible on all views.
@register.simple_tag
def get_all_language_groups():
    return ProjectLanguage.objects.all()