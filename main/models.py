from django.db import models


class Auths(models.Model):
    id=models.IntegerField(primary_key=True)
    email=models.EmailField()
    UserName=models.CharField(max_length=50)
    password=models.CharField(max_length=10)
    data_add=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    role=models.CharField(max_length=10)
    last_visit=models.DateTimeField()
    is_confirm=models.BooleanField()
    EmailConfirmed=models.BooleanField()

    class Meta:
        db_table='public\".\""Auths"'


class EmployeeOwners(models.Model):
    id=models.IntegerField(primary_key=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    middlename=models.CharField(max_length=100)
    phone=models.CharField(max_length=11)
    email=models.EmailField()
    link=models.CharField(max_length=15)
    date_add=models.DateTimeField(auto_now_add=True)
    birthday=models.DateField()
    position=models.CharField(max_length=30)
    id_owner=models.IntegerField()
    accepted=models.BooleanField()
    id_user=models.ForeignKey(Auths, on_delete=models.CASCADE, db_column='id_user')

    class Meta:
        db_table = 'public\".\"EmployeeOwners'


class dayOfWorks(models.Model):
    id=models.IntegerField(primary_key=True)
    dttmStart=models.DateTimeField()
    dttmEnd=models.DateTimeField()
    accountId=models.IntegerField()
    class Meta:
        db_table = 'public\".\"dayOfWorks'

    def __str__(self):
        return '{0}-{1}'.format(self.dttmStart, self.dttmEnd)


class Tokens(models.Model):
    id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(Auths, on_delete=models.CASCADE, db_column='user_id')
    access=models.CharField(max_length=255)
    refresh = models.CharField(max_length=255)
    access_generate=models.DateTimeField()
    refresh_generate=models.DateTimeField()
    access_expire=models.DateTimeField()
    refresh_expire=models.DateTimeField()
    class Meta:
        db_table='public\".\"Tokens'

class Accounts(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    id_user = models.ForeignKey(Auths, on_delete=models.CASCADE, db_column='id_user')
    update=models.DateTimeField()

    class Meta:
        db_table = 'public\".\"Accounts'



class conctereDays(models.Model):
    id=models.IntegerField(primary_key=True)
    services_id=models.IntegerField()
    dttm_start=models.DateTimeField()
    dttm_end=models.DateTimeField()
    price=models.FloatField()
    comment=models.TextField()
    daysof=models.ForeignKey(dayOfWorks, on_delete=models.CASCADE, db_column='daysof')
    class Meta:
        db_table = 'public\".\"conctereDays'



class Clients(models.Model):
     id=models.IntegerField(primary_key=True)
     name=models.CharField(max_length=100)
     phone=models.CharField(max_length=11)
     email=models.EmailField()
     desc=models.TextField()
     id_user=models.ForeignKey(Auths, on_delete=models.CASCADE, db_column='id_user')
     status=models.CharField(max_length=20)
     class Meta:
        db_table = 'public\".\"Clients'
# Create your models here.
