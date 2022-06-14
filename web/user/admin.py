from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User



class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('name',)}),
    ) + AuthUserAdmin.fieldsets
    fieldsets = (
            ('User Profile', {'fields': ('name', 'current_session')}),
    ) + AuthUserAdmin.fieldsets

    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']



# @admin.register(Reviewer)
# class ReviewerAdmin(admin.ModelAdmin):

#     list_display = (..., 'get_username',  'last_active_time')

#     def get_username(self, obj):
#         return obj.user.username

#     get_username.short_description = 'UserName'

    # search_fields = ['name']