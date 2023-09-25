from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe

class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="cat",alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image= models.ImageField(upload_to="category")

    # for the admin panel
    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

