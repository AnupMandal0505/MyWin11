from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migration=True

    def _create_user(self,phone,email,password=None,**extra_fields):
        if not phone and not email:
            raise ValueError("You have not provided a valid USER PHONE NUMBER or EMAIL")
        email = self.normalize_email(email)
        user=self.model(phone=phone,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self,phone,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(phone,password,**extra_fields)
        

    def create_superuser(self,phone,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(phone,email,password,**extra_fields)