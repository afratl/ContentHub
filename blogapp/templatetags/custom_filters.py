from django import template

register = template.Library()

def hosgeldin(value):
    return f'Merhaba {value}'

register.filter(hosgeldin)