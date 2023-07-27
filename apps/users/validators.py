from django.core.validators import RegexValidator
PhoneValidator = RegexValidator(regex=r"^996(\d{3})\d{2}\d{2}\d{2}$")
