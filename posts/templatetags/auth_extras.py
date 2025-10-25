from django import template

try:
    from allauth.socialaccount.models import SocialApp
except Exception:  # allauth may not be installed in some contexts
    SocialApp = None

register = template.Library()

@register.simple_tag
def has_social_app(provider: str) -> bool:
    """Return True if a SocialApp is configured for the given provider.
    Safe to call even if allauth is not installed.
    """
    if SocialApp is None:
        return False
    return SocialApp.objects.filter(provider=provider).exists()
