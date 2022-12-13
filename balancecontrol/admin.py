from django.contrib import admin

from .models import Balance


# Register your models here.
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('value', 'typeoperation', 'datecreate')
    list_filter = ('typeoperation', 'datecreate')
    list_editable = ('typeoperation',)
    search_fields = ('typeoperation', 'datecreate')
    list_per_page = 10


admin.site.register(Balance, BalanceAdmin)
