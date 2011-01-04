from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_registry import UserRegistry


from duct_tape.models.decorators import register_pre_and_post_signal

from datetime import datetime

class TimeStampedModelBase(models.Model):
    """
    This is an abstract Model used to provide
        created_at
        updated_at
    """
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True, blank=False, null=False)

    class Meta:
        abstract = True

class DeletableModelBase(models.Model):
    """
    This is an abstract Model used to provide
        delete (+ pre_delete & post_delete signals), 
        restore, (+ pre_restore & post_restore signals), 
        purge ( the original model.delete & its signals), 
        deleted_at and is_deleted()

    Its actually a misnomer because it allows an object to go into a deleted state
        but is never actually deleted
    """
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)


    def delete(self):
        '''
        Overrides the existing model.Model.delete()
        
        Sets a deleted_at = DateTimeStamp

        fires signals DeletableModelBase.pre_delete and post_delete
        '''
        self.deleted_at = datetime.now()
        self.save()

    def restore(self,*args,**kwargs):
        '''
        *restores* the object by setting its deleted_at attr to None

        fires signals DeletableModelBase.pre_restore and post_restore
        '''
        self.deleted_at = None
        self.save()

    def purge(self,*args,**kwargs):
        '''
        calls the original model.Model.delete
        '''
        super(DeletableModelBase,self).delete(*args,**kwargs)

    def is_deleted(self):
        return self.deleted_at != None
    
    class Meta:
        abstract = True

register_pre_and_post_signal(DeletableModelBase,['delete','restore'])

class CreatedByModelBase(models.Model):
    """
    This is an abstract Model used to provide
        created_by
        has_creator flag (which is used by CreatedByModelFormMixin)
    """
    created_by = models.ForeignKey(User, related_name='+', editable=False, blank=True, null=True)

    # capture which classes signals need to be listening for
    _class_signal_dict = {}

    @classmethod
    def __new__(klass,*args,**kwargs):
        kls = super(CreatedByModelBase,klass).__new__(klass)
        if not klass in CreatedByModelBase._class_signal_dict:
            dispatch_uid = "createdbymodelbase_auto_add_creator__%s.%s" % (klass.__module__, klass.__name__)

            # we don't need to keep the dispatch_uid around but it doesn't hurt
            CreatedByModelBase._class_signal_dict[klass] = dispatch_uid

            post_save.connect(CreatedByModelBase.auto_add_creator,sender=klass,weak=False,dispatch_uid=dispatch_uid)

        return kls
    
    @classmethod
    def auto_add_creator(klass,sender,**kwargs):
        instance = kwargs['instance']
        created = kwargs['created']

        if UserRegistry.has_user() and created:
            instance.created_by = UserRegistry.get_user()
            instance.save()

    def has_creator(self):
        return not self.created_by==None
    
    class Meta:
        abstract = True

