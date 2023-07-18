from django.contrib import admin
from apps.product.models import (Postcard, Flowers, SweetGift, Balloon)

admin.site.register(Postcard)
admin.site.register(Flowers)
admin.site.register(SweetGift)
admin.site.register(Balloon)
