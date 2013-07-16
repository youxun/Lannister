from django.conf import settings
gettext = lambda s: s



BOOSTRAP_DEFAULT = getattr(settings,
                           'BOOSTRAP_DEFAULT',
						   {'class':'required'})

BOOSTRAP_TEXTINPUT = getattr(settings,
                           'BOOSTRAP_TEXTINPUT',
						   {'class':'required','placeholder':'Text input'})
BOOSTRAP_PASSWORD = getattr(settings,
                           'BOOSTRAP_PASSWORD',
						   {'class':'required','id':'inputPassword','placeholder':'Password'})
BOOSTRAP_CHECKBOX = getattr(settings,
                           'BOOSTRAP_CHECKBOX',
						   {'class':'required'})						  