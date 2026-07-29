from django.contrib import admin

from .models import (
    Booking,
    BudgetGroup,
    Expense,
    Hotel,
    Member,
)


@admin.register(BudgetGroup)
class BudgetGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group")
    search_fields = ("name",)
    list_filter = ("group",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "amount",
        "paid_by",
        "group",
        "date",
    )

    search_fields = (
        "title",
        "paid_by__name",
    )

    list_filter = (
        "group",
        "date",
    )


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "price",
    )

    search_fields = (
        "name",
        "city",
    )

    list_filter = (
        "city",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hotel_name",
        "city",
        "status",
        "check_in",
        "check_out",
    )

    search_fields = (
        "name",
        "hotel_name",
        "email",
    )

    list_filter = (
        "status",
        "city",
    )