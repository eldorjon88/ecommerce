from django.db import models
from django.conf import settings
from apps.products.models import Product

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'product')  # 1 user 1 productga 1 ta review

    def __str__(self):
        return f'{self.user} → {self.product} ({self.rating})'

    def to_dict(self):
        return {
            "id": self.pk,
            "user": self.user.username,
            "product": self.product_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
        }

