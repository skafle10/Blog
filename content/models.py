
from django.db import models
from django.conf import settings
from django.utils.text import slugify
# Create your models here.


class BlogPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnails/%y/%m/%d',max_length=100)
    slug = models.SlugField(null=False, unique=True, max_length=255)
    writer = models.CharField(max_length=90)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            base_slug = self.slug
            slug_index = 0
            
            while (BlogPost.objects.filter(slug=self.slug).exists()):
         
                    slug_index += 1
                    self.slug = f"{base_slug}-{slug_index}"

        super().save(*args,**kwargs)
    
    


