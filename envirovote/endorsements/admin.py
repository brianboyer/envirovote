from django.contrib import admin
from envirovote.endorsements.models import Organization, Endorsement

class OrganizationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Organization, OrganizationAdmin)

class EndorsementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Endorsement, EndorsementAdmin)
