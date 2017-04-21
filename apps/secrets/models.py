from __future__ import unicode_literals
from django.db.models import Count
from django.db import models
from ..loginReg.models import User
from datetime import datetime

# Create your models here.
class SecretManager(models.Manager):

    def ValidateAndSave(self, request):
        errors = []

        if len(request.POST['secret']) == 0:
            errors.append("You'll need to write something")

        if len(request.POST['secret']) > 255:
            errors.append("Sorry, please keep your secret less than 255 characters")

        if len(errors) == 0:
            currentUser = Secret.objects.GetCurrentUser(request.session['id'])
            try:
                objSecret = Secret.objects.create(
                    content = request.POST['secret'],
                    created_by = currentUser,
                    created_at = datetime.now(),
                    updated_at = datetime.now()
                )
                context = {
                    "secret": objSecret
                }
                return (True, context)
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
                errors.append(e.message)
                return (False, errors)
        else:
                return (False, errors)

    def GetLatestSecrets(self):
        print "func GetLatestSecrets"
        objReturn = Secret.objects.all().order_by('-created_at')[:5]
        # print objReturn

        return objReturn

    def GetCurrentUser(self, data):
        print "func GetCurrentUser"
        try:
            usrReturn = User.objects.get(id=data)

            return usrReturn
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return e

    def DeleteSecret(self, request, data):
        print "func DeleteSecret"
        currentUser = self.GetCurrentUser(request)
        try:
            objDelete = Secret.objects.get(id=data)
            if objDelete.created_by == currentUser:
                objDelete.delete()
            return True
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return e.message

    def LikeSecret(self, user_id, data):
        print "func LikeSecret"
        currentUser = self.GetCurrentUser(user_id)
        try:
            objLike = Secret.objects.get(id=data)
            objLike.liked_by.add(currentUser)
            objLike.save()
            return True
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return e.message

    def GetMostPopularSecrets(self):
        print "func GetMostPopularSecrets"
        objReturn = Secret.objects.annotate(likes=Count('liked_by')).order_by('-likes')

        return objReturn


class Secret(models.Model):
    content = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creators")
    liked_by = models.ManyToManyField(User, related_name="fans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
