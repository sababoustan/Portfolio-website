from django.contrib import admin
from .models import Comment


# Register your models here.
class ReplyInline(admin.TabularInline):
    model = Comment
    fk_name = "parent"
    extra = 1
    verbose_name = "پاسخ"
    verbose_name_plural = "پاسخ‌ها"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "body", "is_active", "created_at")
    list_filter = ("is_active", "product")
    search_fields = ("user__username", "body")
    inlines = [ReplyInline]
    
    def save_model(self, request, obj, form, change):
        if request.user.is_staff:
            obj.is_active = True
        super().save_model(request, obj, form, change)
