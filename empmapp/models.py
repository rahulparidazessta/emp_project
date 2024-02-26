from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

# Employee model represents individual employees in the system
class Employee(models.Model):
    Name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    phone_num = models.CharField(max_length=10)
    department = models.ForeignKey('Department', on_delete=models.CASCADE,related_name='employees') #models.foreignkey refers to many_to_one relationship
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(storage=S3MediaStorage(),blank=True,null=True)


    def __str__(self) :
        return self.Name

# Dept model represents Dept in the system
class Department(models.Model):
    Name = models.CharField(max_length=15)
    supervisor_name = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self) :
        return self.Name


class AttendenceDetails(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE,)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_timee = models.TimeField()
    Present = models.BooleanField()
    # present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.Name} - {self.date}"

