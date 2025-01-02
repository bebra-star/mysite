from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from main.managers import UserManager


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    flag = models.CharField(max_length=1)


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    objects = UserManager()
    first_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="first_language"
    )
    second_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="second_language"
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]


class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    language1 = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="language1"
    )
    language2 = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="language2"
    )


class WordPair(models.Model):
    id = models.AutoField(primary_key=True)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    word1 = models.CharField(max_length=30)
    word2 = models.CharField(max_length=30)


class TestSession(models.Model):
    id = models.AutoField(primary_key=True)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_word_index = models.IntegerField()
    is_showing_language_first = models.BooleanField()


class TestSessionWordPairStatus(models.IntegerChoices):
    SKIPPED = 0
    NOT_LEARNED = 1
    LEARNED = 2


class TestSessionWordPair(models.Model):
    id = models.AutoField(primary_key=True)
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    word_pair = models.ForeignKey(WordPair, on_delete=models.CASCADE)
    status = models.IntegerField(
        default=None, choices=TestSessionWordPairStatus.choices, blank=True, null=True
    )
