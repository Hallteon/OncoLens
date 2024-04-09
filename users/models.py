import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser


class Patient(models.Model):
    firstname = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, verbose_name='Отчество')
    birthday = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата создания')

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.surname}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class OrganizationCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория организации'
        verbose_name_plural = 'Категории организаций'


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey('OrganizationCategory', on_delete=models.DO_NOTHING,
                                 related_name='organizations_category', verbose_name='Категория')
    employees = models.ManyToManyField('CustomUser', related_name='organizations_employee',
                                       verbose_name='Сотрудники')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    role_type = models.CharField(max_length=255, unique=True, verbose_name='Тип роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('User must have an username')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255, verbose_name='Логин')
    firstname = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, verbose_name='Отчество')
    role = models.ForeignKey('Role', blank=True, null=True, on_delete=models.CASCADE, related_name='users_role', verbose_name='Роль')
    speciality = models.ForeignKey('Speciality', blank=True, null=True, on_delete=models.CASCADE, related_name='users_speciality',
                                   verbose_name='Специальность')
    patients = models.ManyToManyField('Patient', related_name='users_patient', verbose_name='Пациенты')
    correct_answers = models.IntegerField(default=0, verbose_name='Количество правильных снимков')
    incorrect_answers = models.IntegerField(default=0, verbose_name='Количество неправильных снимков')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    password = models.CharField(max_length=255, verbose_name='Пароль')

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'