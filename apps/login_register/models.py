from __future__ import unicode_literals
from django.db import models
import datetime # use for birthday checks/ times/ dates
import re 
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def currentUser(self, request):
        id = request.session['user_id']

        return User.objects.get(id=id)

    def validateRegistration(self, form_data):
        errors = []

        if len(form_data['name']) == 0:
            errors.append("Name is required.")
        if not form_data['name'].isalpha():
            errors.append("Name cant contain numbers.")
        if len(form_data['alias']) == 0:
            errors.append("Alias is required.")
        if not form_data['alias'].isalpha():
            errors.append("Alias cant contain numbers.")
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append("Please enter a valid email.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        if form_data['password'] != form_data['confirm_password']:
            errors.append("Passwords do not match.")

        #birthday if needed
        now = datetime.datetime.now()
        birthday = datetime.datetime.strptime(form_data['birthday'], '%Y-%m-%d')
        if birthday > now:
          errors.append("Birthday can not be in the future.")

        return errors

    def validateLogin(self, form_data):
        errors = []

        user = User.objects.filter(email = form_data['email']).first()

        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        if user == []:
            errors.append('Accounts does not exit. Please register.')

        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = hashed_pw,
            birthday = form_data['birthday']
        )

        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    
    # birthday if needed.
    birthday = models.DateField(null=True, blank=True)
    
    # Self joining example. User has many friends and for the related name it is friended by.
    # Self joining can only be done once(ex: you can only like once on facebook but poke
    # as many times as you want) that would be many to many for multiple times
    friends = models.ManyToManyField("self", related_name="friend_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


# another way of doing many to many

# class Friend(models.Model):
#   user = models.ForeignKey(User)
#   friend = models.ForeignKey(User)
