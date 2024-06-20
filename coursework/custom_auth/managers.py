from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, phone=None, \
                     password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            if not phone:
                raise ValueError('The given email/phone must be set')

        if phone:
            if not username:
                username = phone

            user = self.model(
                username=username,
                phone=phone,
                **extra_fields
            )

        # проверяем является ли пользователь
        # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                username=username,
                phone=phone,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, phone=phone, password=password, **extra_fields)

    def create_superuser(self, username,phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        print(f'Здесь {phone}!!!!!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username=username, phone=phone, password=password, **extra_fields)