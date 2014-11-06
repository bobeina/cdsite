#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    	content = models.CharField(max_length=600,blank=True,null=True)
	username = models.ForeignKey(User, related_name='msg_uid')
	date = models.DateTimeField(auto_now_add=True)
	cmd = models.CharField(max_length=10)
	target = models.IntegerField(blank=True,null=True)
	cmdType = models.CharField(max_length=3)
	gid = models.IntegerField(blank=True,null=True)
	#(
	#		(u'pub',u'public'),
	#		(u'pri',u'private'),
	#		(u'gam',u'game'),
	#		(u'sys',u'system'),
	#		(u'ano',u'announcement'),
	#	)
	


# pc online list
class PC(models.Model):
	player = models.ForeignKey(User, related_name='online_uid')
	active_time = models.DateTimeField(auto_now = True)
	active_time.editable = True
	ip = models.CharField(max_length = 16)
	gameStatue = models.IntegerField(blank=True,null=True) # 0: free; gameInfo_id: playing cthulhu game (#gameInfo_id)
	sanity = models.IntegerField()
	
class Counter(models.Model):
	player = models.ForeignKey(User,related_name = 'connter_uid')
        totalwin = models.IntegerField()
        totalgame = models.IntegerField()

class GameInfo(models.Model):
        cthulhuSanity = models.IntegerField(blank=True,null=True) 
	pclist = models.CharField(max_length = 60)
	winner = models.IntegerField(blank=True,null=True)
	statue = models.IntegerField()					# waiting for players:1, gaming:2, finished: 0
        createTime = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User,related_name = 'creator_uid')


class Round(models.Model):
	gameID = models.ForeignKey(GameInfo,related_name = 'r_gid');
	roundNum = models.IntegerField(blank=True,null=True)
	caster = models.IntegerField(blank=True,null=True)
	victim = models.IntegerField(blank=True,null=True)
	attackTimeBegin = models.DateTimeField(blank=True,null=True)
	fbTimeBegin = models.DateTimeField(blank=True,null=True) # fight back
	#dice: -1: not roll yet; 0: TimeOut;
	# 1: Cthulhu; 2:Tentacle; 3:Yellow; 4:Elder; 5:Eye
	casterDice = models.IntegerField(blank=True,null=True)
	victimDice = models.IntegerField(blank=True,null=True)
	roundStatue = models.IntegerField(blank=True,null=True)#0:unfinish 1: finished


