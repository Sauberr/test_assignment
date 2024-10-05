from django.db import models
from faker import Faker
from subscriptions.models import Subscription


class Images(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=200)
    description = models.TextField()
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name: str = "Image"
        verbose_name_plural: str = "Images"

    def __str__(self):
        return self.title

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                title=faker.sentence(),
                image=faker.image_url(),
            )
