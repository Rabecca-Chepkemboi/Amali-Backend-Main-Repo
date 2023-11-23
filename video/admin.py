# from django.contrib import admin
# from.models import Video

# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('athlete', 'description', 'download_link')
#     list_filter = ('athlete',)
#     search_fields = ('athlete__full_name', 'description')

#     def athlete(self, obj):
#         return obj.athlete.full_name
#     athlete.short_description = 'Athlete'
