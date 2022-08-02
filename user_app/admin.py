from django.contrib import admin
# Register your models here.
from user_app.api.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'phonenumber','contact_through')}),
        (_('permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),

        }),
    )
    list_display = ['email', 'username', 'is_staff', 'phonenumber','contact_through']
    search_fields = ('email', 'first_name')


admin.site.register(User, UserAdmin)