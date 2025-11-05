import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar_url(email, size=100):
    email = email.strip().lower().encode('utf-8')
    hash_email = hashlib.md5(email).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}?s={size}&d=identicon"
