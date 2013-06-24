from django.db import models
from django.contrib.auth.models import User
from django import forms

class Utilisateur(models.Model):
	profilBase = models.OneToOneField(User, primary_key=True, related_name='profilBaseInUtilisateur')
	
	def __unicode__(self):
		return (self.profilBase.first_name+" "+self.profilBase.last_name+" @ "+self.profilBase.email)

	def __repr__(self):
		return self.__unicode__()

class WatchLater(models.Model):
	ID = models.CharField(max_length=100)
	relationUtilisateur =models.ForeignKey(Utilisateur) 

class FavoriteArticle(models.Model):
	ID = models.CharField(max_length=100)
	relationUtilistateur = models.ForeignKey(Utilisateur)