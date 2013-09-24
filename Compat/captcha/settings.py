from django.conf import settings
import os.path

# The directory where captcha files will store.
CAPTCHA_STORE = getattr(settings, 'CAPTCHA_STORE', os.path.join(os.path.dirname(__file__), 'data'))
CAPTCHA_FONTS = getattr(settings, 'CAPTCHA_FONTS', os.path.join(os.path.dirname(__file__), 'fonts'))
CAPTCHA_BGCOLOR = getattr(settings, 'CAPTCHA_BGCOLOR', (42, 59, 168))
CAPTCHA_FGCOLOR = getattr(settings, 'CAPTCHA_BGCOLOR', (255, 255, 255))
CAPTCHA_LIVING = getattr(settings, 'CAPTCHA_LIVING', 3600*12)
