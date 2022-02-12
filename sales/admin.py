from django.contrib import admin

# Manage four database forms through the administrator interface
# Username and password of staff created from administrator interface 
 
from .models import Staff
from .models import Beverage
from .models import Record
from .models import User

admin.site.register(Staff)
admin.site.register(Beverage)
admin.site.register(Record)
admin.site.register(User)