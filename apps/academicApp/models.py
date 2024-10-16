from django.db import models

# Create your models here.

class Area(models.Model):
    area_name = models.CharField(max_length=200)

    def __str__(self):
        return self.area_name


class Career(models.Model):
    career_name = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.career_name
    

class Signature(models.Model):
    signature_name = models.CharField(max_length=200)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    def __str__(self):
        return self.signature_name


class Section(models.Model):
    section_name = models.CharField(max_length=200)
    semester = models.IntegerField()
    teacher_guide = models.ForeignKey('userApp.Profile', on_delete=models.CASCADE, related_name='section_of_teacher_guide')
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_name