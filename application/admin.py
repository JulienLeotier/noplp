"""
file admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    """
    Create view for django admin
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'pseudo','use',)
    list_filter = ('email', 'is_staff', 'is_active', 'pseudo', 'use',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'pseudo', 'avatar', 'use',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'pseudo', 'avatar', 'use',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class MusiqueAdmin(admin.ModelAdmin):
    models = Musique
    list_display = ('name', 'author', 'categorie',)
    list_filter = ('name', 'author', 'categorie',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categorie)
admin.site.register(Historique)
admin.site.register(Musique, MusiqueAdmin)
