from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyAccountManager






class Account(AbstractBaseUser):
       first_name = models.CharField(max_length=50)
       last_name = models.CharField(max_length=50)
       email = models.EmailField(max_length=100, unique = True)
       phone_number = models.CharField(max_length=100, unique=True)



       # required

       date_joined = models.DateTimeField(auto_now_add=True)
       last_login = models.DateTimeField(auto_now_add=True)
       is_admin = models.BooleanField(default=False)
       is_staff = models.BooleanField(default=False)
       is_active = models.BooleanField(default=False)
       is_superadmin = models.BooleanField(default=False)




       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name' ]

       object = MyAccountManager()

       def __str__(self):
           return self.email



       def has_perm(self, perm, obj=None):
              return self.is_admin



       def has_module_perms(self, add_label):
              return True

              

       def fullname(self):
              return f"".format(self.first_name,self.last_name)
    
    



class VerificationUser(models.Model):
       user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'verification_user')
       otp = models.IntegerField(blank=True, null=True)
       otp_verification = models.BooleanField(default=False)
       email_verification = models.BooleanField(default=False)
       otp_attempt = models.IntegerField(default=0)
       otp_sent_date = models.DateTimeField(auto_now=True)
       verification_date = models.DateTimeField(auto_now=True)


       def __str__(self):
              return self.user.email



