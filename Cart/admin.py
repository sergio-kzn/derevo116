from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


class CityInlines(admin.TabularInline):
    model = City


class CountryAdmin(admin.ModelAdmin):
    inlines = [CityInlines]


class DeliveryAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


class ItemInlines(admin.TabularInline):
    model = Item


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInlines]
    readonly_fields = ['order_number']


admin.site.register(Country, CountryAdmin)
admin.site.register(City)
admin.site.register(Order, OrderAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Payment)
admin.site.register(Status)
admin.site.register(Item)
