from django.contrib import admin

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('menu', 'name', 'slug', 'parent')
    list_filter = ('menu', 'name', 'slug', 'parent')
    search_fields = ('menu', 'name', 'slug', 'parent')