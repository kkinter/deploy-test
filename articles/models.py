from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from .utils import get_latitude_longitude


# Create your models here.
class Restaurant(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    address = models.TextField()
    address_detail = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True, max_length=500)
    phone_number = models.CharField(max_length=30, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    cusine_code = models.IntegerField(null=True)
    subcusine_code = models.IntegerField(null=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_restaurant"
    )
    # tags=models.ManyToManyField('Tag', blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.latitude, self.longitude = get_latitude_longitude(self.address)
        super(Restaurant, self).save(*args, **kwargs)

class ArticleComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    content = models.TextField()
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 유저, 추천 추가하기 이미지 여러개 모델 추가해서 fk 넣기

# class Tag(models.Model):
#     name=models.CharField(max_length=10)

#     def __str__(self) : 
#         return self.name #해시태그를 자신의 이름으로 보여준다