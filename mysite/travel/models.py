from django.db import models


class BudgetGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Member(models.Model):
    group = models.ForeignKey(
        BudgetGroup,
        on_delete=models.CASCADE,
        related_name="members"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.group.name})"


class Expense(models.Model):
    group = models.ForeignKey(
        BudgetGroup,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True, null=True)

    city = models.CharField(max_length=100, default="Hyderabad")
    hotel_name = models.CharField(max_length=100)

    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        default="Confirmed"
    )

    def __str__(self):
        return f"{self.name} - {self.hotel_name} ({self.status})"