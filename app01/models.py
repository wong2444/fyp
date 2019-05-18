from django.db import models


# Create your models here.


class Course(models.Model):
    c_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class Module(models.Model):
    m_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class User(models.Model):
    s_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50)
    c_id = models.ForeignKey(Course, blank=True, on_delete=models.CASCADE)


class Course_to_Module(models.Model):
    m_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    s_id = models.ForeignKey(User, on_delete=models.CASCADE)  # teacher id
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.PositiveSmallIntegerField()
    class_room = models.CharField(max_length=50)


class Attendance_Record(models.Model):
    c_to_m_id = models.ForeignKey(Course_to_Module, on_delete=models.CASCADE)
    s_id = models.ForeignKey(User, on_delete=models.CASCADE)
    today_date = models.DateField()
    arrive_time = models.TimeField()
    is_late = models.BooleanField()
    is_abs = models.BooleanField()
