from apps.admin.site import admin_site
from apps.models import User, Auditorium, Order


admin_site.register(User)
admin_site.register(Auditorium)
admin_site.register(Order)
