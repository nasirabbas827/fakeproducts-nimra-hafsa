from django.contrib import admin
from .models import user_register, Product, Comment, IPTracking

# Custom Admin for Comment model with restricted permissions
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentid', 'product', 'username', 'comment_date', 'sentiment_label', 'ip_address')
    search_fields = ('product__name', 'username', 'text')
    list_filter = ('sentiment_label', 'comment_date')
    readonly_fields = ('commentid', 'product', 'username', 'text', 'comment_date', 'sentiment_score', 'sentiment_label', 'ip_address')
    
    # Prevent adding or editing comments by removing add and change actions
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # Allow deleting comments
    def has_delete_permission(self, request, obj=None):
        return True

# Custom Admin for IPTracking model with restricted permissions
class IPTrackingAdmin(admin.ModelAdmin):
    list_display = ('ip_id', 'ip_address', 'product', 'review_count', 'flagged_as_fake', 'last_review_date')
    search_fields = ('ip_address', 'product__name')
    list_filter = ('flagged_as_fake', 'last_review_date')
    readonly_fields = ('ip_id', 'ip_address', 'product', 'review_count', 'flagged_as_fake', 'last_review_date')
    
    # Prevent adding or editing IP Tracking records by removing add and change actions
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # Allow deleting IP tracking records
    def has_delete_permission(self, request, obj=None):
        return True

# Register models with their custom Admin
admin.site.register(user_register)
admin.site.register(Product)
admin.site.register(Comment, CommentAdmin)
admin.site.register(IPTracking, IPTrackingAdmin)
