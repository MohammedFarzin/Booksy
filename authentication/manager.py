from django.contrib.auth.models import BaseUserManager






class MyAccountManager(BaseUserManager):
       def create_user(self, first_name, last_name, phone_number,   email, password= None):
              if not email:
                     raise ValueError("User must have an email address")

              
              if not phone_number:
                     raise ValueError("User must have an phone number")


              if not password:
                     raise ValueError("User must have an password")

              
              user = self.model(
                     email = self.normalize_email(email),
                     first_name = first_name,
                     last_name = last_name,
                     phone_number = phone_number, 
              )
              user.set_password(password)
              user.save(using = self._db)
              return user

       def create_superuser(self, first_name, last_name, email,  phone_number, password=None, ):
              user = self.create_user(
                     email = self.normalize_email(email),
                     password = password,
                     first_name = first_name,
                     last_name = last_name,
                     phone_number = phone_number,
              )

              user.is_admin = True
              user.is_active = True
              user.is_staff = True
              user.is_superadmin = True
              user.save(using = self._db)
              return user





