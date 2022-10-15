from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    profile_image = models.ImageField(
        default="default_profile_pic.jpg",upload_to="profile_pics"
    )
    
    intro = models.CharField(max_length=60, blank=True, null=True)
    #self 자기가 자기자신을 다시 참조하는 것이기 때문에 self라는 인자 줌
    #symmetrical은 대칭을 할지 말지를 결정하는 건데 여기서 이 옵션에 True를 주면 한 사람이 어떤 사람을 팔로우하면 저절로 맞팔이 되게 된다.
    followings = models.ManyToManyField('self', symmetrical=False, blank=True, related_name= 'followers')