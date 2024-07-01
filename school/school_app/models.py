from django.db import models

# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=100)
    club_description = models.TextField()
    club_logo = models.ImageField(upload_to='clubs/')

    def __str__(self): # Panelde Kulüp adı ile göster.
        return self.club_name
    
    
class ClubActivity(models.Model):
    activity_header = models.CharField(max_length=100)
    activity_content = models.TextField()
    activity_image = models.ImageField(upload_to='activities/')
    activity_club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    activity_is_active = models.BooleanField(default=False)
    activity_date = models.DateTimeField()

    def __str__(self):
        return self.activity_header