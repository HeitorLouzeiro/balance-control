from django.contrib import admin

from .models import PassawordResetToken


# Register your models here.
class PassawordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'datecreate',)
    list_filter = ('token', 'datecreate',)
    search_fields = ('token' 'datecreate', 'expire_at')


admin.site.register(PassawordResetToken, PassawordResetTokenAdmin)
