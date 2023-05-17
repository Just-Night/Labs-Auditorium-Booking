from django.db import models


class Auditorium(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    seats = models.IntegerField()
    address = models.CharField(max_length=150)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"address: {self.address}; id:{self.id}"


class Order(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='orders')
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name='orders')
    reservation_date = models.DateField()
    start_datetime = models.TimeField(null=True)
    end_datetime = models.TimeField(null=True)

    class Meta:
        unique_together = [
            [
                'reservation_date',
                'start_datetime'
            ],
            [
                'reservation_date',
                'end_datetime'
            ]
        ]
