from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "payment_method", "payment_date", "status", "created_at"]
    fields = [
        "user",
        "order",
        "pg_result",
        "payment_id",
        "payment_date",
        "pg_salt",
        "pg_description",
        "pg_failure_description",
        "currency",
        "payment_method",
        "amount",
        "pg_card_pan",
        "pg_sig",
        "status",
        "created_at"
    ]
    readonly_fields = fields
    ordering = ["-created_at"]
    search_fields = ["order__payment_type", "user__full_name", "order__order_id"]
    list_filter = ["status"]
    list_per_page = 25

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
