from django.contrib import admin
from .models import Profile, Relation


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age')
    search_fields = ('user', 'age', 'location')
    list_filter = ('user', 'age', 'location')
    raw_id_fields = ('user',)


admin.site.register(Profile, ProfileAdmin)


class RelationAmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')



admin.site.register(Relation, RelationAmin)
