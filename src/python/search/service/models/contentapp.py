'''
###############################################
#  MODELS FOR BILLING SYSTEM
###############################################
'''
from django.db import models

class City(models.Model): # pylint: disable=C1001
    ''' Store All City '''
    id = models.AutoField(primary_key=True)
    name = models.CharField('City Name', max_length=128,\
           null=False, blank=False, unique=True)
    slug_name = models.SlugField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta: # pylint: disable=C1001
        ''' Table Name '''
        db_table = 'city'
        verbose_name = 'City'
        verbose_name_plural = 'City'

    def __unicode__(self):
        return self.name

class DropPoint(models.Model): # pylint: disable=C1001
    ''' Center where News Paper is Distributed '''
    id = models.AutoField(primary_key=True)
    name = models.CharField('Drop Point', max_length=128,\
           null=False, blank=False, unique=True)
    slug_name = models.SlugField(max_length=255, blank=True)
    city = models.ForeignKey(City, verbose_name='City')
    is_active = models.BooleanField(default=True)

    class Meta: # pylint: disable=C1001
        ''' Table Name '''
        db_table = 'droppoint'
        verbose_name = 'DropPoint'
        verbose_name_plural = 'DropPoint'

    def __unicode__(self):
        return self.name

class Agent(models.Model): # pylint: disable=C1001
    '''Agents that Perchase or Going to Perchase'''
    id = models.AutoField(primary_key=True)
    name = models.CharField('Agent Name', max_length=128, \
           null=False, blank=False)
    area = models.ForeignKey(DropPoint, verbose_name='DropPoint')
    is_active = models.BooleanField(default=True)

    class Meta: # pylint: disable=C1001
        ''' Table Name '''
        db_table = 'agent'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        unique_together = ['name', 'area']

    def __unicode__(self):
        return self.name

class NewsPaper(models.Model): # pylint: disable=C1001
    ''' All the News Paper Distributed '''
    id = models.AutoField(primary_key=True)
    name = models.CharField('News Paper', max_length=128, \
           null=False, blank=False)
    name_slug = models.SlugField(max_length=255, blank=True)
    abbrevation = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta: # pylint: disable=C1001
        ''' Table Name  '''
        db_table = 'newspaper'
        verbose_name = 'NewsPaper'
        verbose_name_plural = 'NewsPapers'

    def __unicode__(self):
        return self.name

class AgentSubscription(models.Model): # pylint: disable=C1001
    ''' Papers Percahsed by an agent '''
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(DropPoint, verbose_name='DropPoint')
    agent = models.ForeignKey(Agent, verbose_name='Agent')
    news_paper = models.ForeignKey(NewsPaper, verbose_name='NewsPaper')

    class Meta: # pylint: disable=C1001
        ''' Table Name '''
        db_table = 'agent_subscription'
        verbose_name = 'agent_subscription'
        verbose_name_plural = 'agent_subscriptions'

    def __unicode__(self):
        return str(self.area.name) + ' ' +str(self.agent.name) \
            + ' ' + str(self.news_paper.name)

WEEKDAYS = ((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), \
            (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), \
            (6, 'Sunday'))

class Price(models.Model): # pylint: disable=C1001
    '''Price of a news paper on daily basis'''
    id = models.AutoField(primary_key=True)
    news_paper = models.ForeignKey(NewsPaper, verbose_name='NewsPapers')
    price = models.CharField('Price', max_length=128, \
            null=False, blank=False, unique=True)
    day = models.CharField('Week Day', max_length=20, \
          null=False, blank=False, default='Regular', choices=WEEKDAYS)

    class Meta: # pylint: disable=C1001
        '''Table Name '''
        db_table = 'price'
        verbose_name = 'Price'
        verbose_name_plural = 'price'

    def __unicode__(self):
        return str(self.news_paper) + '' + str(self.price)

class Indent(models.Model): # pylint: disable=C1001
    ''' Number papers Perchased by an agent '''
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(verbose_name='Date')
    agent = models.ForeignKey(Agent, verbose_name='Agent')
    newspaper = models.ForeignKey(NewsPaper, verbose_name='New Paper')
    indent = models.IntegerField(verbose_name='Daily Indent')

    class Meta: # pylint: disable=C1001
        ''' Table Name'''
        db_table = 'indent'
        verbose_name = 'Indent'
        verbose_name_plural = 'Indent'

    def __unicode__(self):
        return str(self.date) + ' ' +str(self.agent.name) + ' '+ str(self.indent)
