from django.db import models
# from register.models import Athlete

class Comment(models.Model):
    # athlete = models.ForeignKey('Athlete', on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=255)
    comment = models.TextField()
    likes = models.IntegerField()

    def __str__(self):
        return self.comment
        

    def add_like(self):
        self.likes += 1
        self.save()
