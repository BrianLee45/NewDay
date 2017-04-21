# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-A0-9._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):

    def ValidateAndLogin(self, request):
        print "ValidateAndLogin"
        errors = []

        if not EMAIL_REGEX.match(request['email']):
            errors.append("Email must be valid email format")

        if len(request['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        if len(errors) != 0:
            return(False, errors)
        else:
            try:
                print request['email']
                userObj = User.objects.get(email=request['email'])
                print "flag 1"
                print userObj.first_name
                if userObj:
                    if bcrypt.checkpw(request['password'].encode('utf-8'), userObj.password.encode('utf-8')):
                        print "Password match"
                        context = {
                        "user": userObj
                        }
                        # return (True, userObj)
                        return (True, context)
                    else:
                        print "Email not found"
                        errors.append("Email/Password not correct")
                        return(False, errors)
            except:
                errors.append("Email/Password not correct")
                return(False, errors)

    def ValidateAndCreate(self, request):
        print "Function ValidateAndCreate"

        errors = []

        if len(request['firstname']) < 2:
            errors.append("First name must be longer than 2 characters")

        if len(request['lastname']) < 2:
            errors.append("Last name must be longer than 2 characters")

        #matches regex
        if not EMAIL_REGEX.match(request['email']):
            errors.append("Email must be valid email format")

        if len(request['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        elif len(request['confirmPass']) < 8:
            errors.append("Password must be at least 8 characters long")

        if request['password'] != request['confirmPass']:
            errors.append("Passwords must match")

        #Check if entered login exists in DB
        try:
        # if len(errors) == 0:
            print request['email']
            userObj = User.objects.get(email=request['email'])
            errors.append("Choose a different login.")
            return (False, errors)
        except Exception as e:
        # else:
            print '%s (%s)' % (e.message, type(e))
            # .get returned 0, so we're good
            if len(errors) == 0 and e.message == 'User matching query does not exist.':
                hashedPW = bcrypt.hashpw(request['password'].encode('utf-8'), bcrypt.gensalt())
                print hashedPW
                #register
                varReturn = User.objects.create(
                    first_name = request['firstname'],
                    last_name = request['lastname'],
                    email = request['email'],
                    password = hashedPW
                )
                context = {
                    "user": varReturn
                }
                print "varReturn.id: " + str(varReturn.id)

                return (True, context)
            else:
                return (False, errors)

    def GetUser(self, data):
        # context = {
        #     "user": User.objects.filter(id=data)
        # }
        objUser = User.objects.filter(id=data)

        print objUser[0].first_name

        return objUser

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
