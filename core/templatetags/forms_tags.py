from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='render_form')
def render_form(form):
    rendered = ''.join([
        field.as_widget(attrs={"class": "form-control mb-3"})
        for field in form
    ])
    return mark_safe(rendered)