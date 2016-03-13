from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('City Name', max_length=128, null=False, blank=False, unique=True)
    slug_name = models.SlugField( max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'city'
        verbose_name = 'City'
        verbose_name_plural = 'City'

    def __unicode__(self):
        return self.name

class DropPoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Drop Point', max_length=128, null=False, blank=False, unique=True)
    slug_name = models.SlugField( max_length=255, blank=True)
    city = models.ForeignKey(City, verbose_name='City')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'droppoint'
        verbose_name = 'DropPoint'
        verbose_name_plural = 'DropPoint'

    def __unicode__(self):
        return self.name

class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Agent Name', max_length=128, null=False, blank=False)
    area = models.ForeignKey(DropPoint, verbose_name='DropPoint')

    class Meta:
        db_table = 'agent'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __unicode__(self):
        return self.name

class NewsPaper(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('News Paper', max_length=128, null=False, blank=False)
    name_slug = models.SlugField(max_length=255, blank=True)
    abbrevation = models.CharField(max_lenth=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'newspaper'
        verbose_name = 'NewsPaper'
        verbose_name_plural = 'NewsPapers'

    def __unicode__(self):
        return self.name

class AgentSubscription(models.Model):
    id=models.AutoField(primary_key=True)
    area = models.ForeignKey(DropPoint, verbose_name='DropPoint')
    agent = models.ForeignKey(Agent, verbose_name='Agent')
    news_paper = models.ForeignKey(NewsPaper, verbose_name='NewsPaper')

    class Meta:
        db_table = 'agent_subscription'
        verbose_name = 'agent_subscription'
        verbose_name_plural = 'agent_subscriptions'

    def __unicode__(self):
        return self.name

WEEKDAYS = ((0, 'Monday'), (1, 'Tuesday'), (2,'Wednesday'), \
            (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), \
            (6, 'Sunday'))

class Price(models.Model):
    id = models.AutoField(primary_key = True)
    news_paper = models.ForeignKey(NewsPaper, verbose_name='NewsPapers')
    price = models.CharField('Price', max_length=128, null=False, blank=False, unique=True)
    day = models.CharField('Week Day', max_length=20, null=False, blank=False, default='Regular', choices=WEEKDAYS)
