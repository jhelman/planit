from planner.models import *
from django.contrib import admin

class RequirementAdmin(admin.ModelAdmin):    
    fields = ['name', 'n_class', 'group', 'bypassable', 'exclusive']
    
    def save_model(self, request, obj, form, change):
        params = request.POST.dict()
        name = params['name']
        if change:
            tag = obj.fulfillers
            tag.name = name
            tag.save()
        else:  
            tags = Tag.objects.filter(name=name)    
            if len(tags) == 1:
                obj.fulfillers = tags[0]
            else:
                tag = Tag(name=name)
                tag.save()
                obj.fulfillers = tag
        obj.save()

admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(University)
admin.site.register(Enrollment)
admin.site.register(Term)
admin.site.register(Plan)
admin.site.register(CourseOffering)
admin.site.register(Major)
admin.site.register(PrereqGroup)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(RequirementGroup)
admin.site.register(TagMapping)