from django.db import models
#from django.contrib.auth.models import AbstractUser
# Create your models here.

#class User(AbstractUser():

class cctv(models.Model):
    user= models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)


class people(models.Model):
    cid=models.IntegerField(default=0)
    up=models.IntegerField(default=0)
    down=models.IntegerField(default=0)

class detect(models.Model):
	did=models.IntegerField(default=0)
	detect_at = models.DateTimeField(auto_now_add = True)

class heatmap(models.Model):
	hid=models.IntegerField(default=0)
	best=models.IntegerField(default=0)
	worst=models.IntegerField(default=0)

# people counting DB 
class PeopleCount(models.Model):
    cid = models.IntegerField()
    up = models.IntegerField()
    down = models.IntegerField()
    date = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'people_count'

