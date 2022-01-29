from django.contrib import admin

from .models import Company, Stock


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker')


class StockAdmin(admin.ModelAdmin):
    list_display = ('company',)


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Stock, StockAdmin)
