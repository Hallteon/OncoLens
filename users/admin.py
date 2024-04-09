from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import *


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'lastname', 'firstname', 'surname')
    search_fields = ('id', 'lastname', 'firstname', 'surname')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category')
    search_fields = ('id', 'name', 'category')
    list_filter = ('name',)


class OrganizationCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type')
    search_fields = ('id', 'name', 'role_type')
    list_filter = ('name',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'firstname', 'lastname', 'surname', 'speciality', 'role',
                    'correct_answers', 'incorrect_answers', 'speciality', 'role', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'firstname', 'lastname', 'surname',
                           'correct_answers', 'incorrect_answers', 'patients', 'speciality', 'role', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'firstname', 'lastname', 'surname',
                       'correct_answers', 'incorrect_answers', 'patients', 'speciality', 'role', 'password1', 'password2'),
        }),)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Patient, PatientAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationCategory, OrganizationCategoryAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)

