from apps.Training.models import TrainingGroup
from django import template

register = template.Library()

# simple tag to make the TrainingGroup menu accessible on all views.
@register.simple_tag
def get_all_training_groups():
    return TrainingGroup.objects.all()