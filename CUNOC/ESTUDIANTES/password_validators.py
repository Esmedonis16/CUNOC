import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "La contraseña debe contener al menos una letra mayúscula."
        )

class DigitValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un dígito."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "La contraseña debe contener al menos un dígito. "
            
        )

class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un símbolo:" +
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "La contraseña debe contener al menos un símbolo:" +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

