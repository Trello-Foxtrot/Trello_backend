from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Workspace, Board, List, Card, Admin, Member

admin.site.register(User)
admin.site.register(Workspace)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)
admin.site.register(Admin)
admin.site.register(Member)
