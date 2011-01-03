from django.db import models
from django.contrib.auth.models import User

from duct_tape.decorators import pre_and_post_signal

from datetime import datetime

class TimeStampedModelBase(models.Model):
    """
    This is an abstract Model used to provide
        created_at
        updated_at
        deleted_at
    """
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True, blank=False, null=False)

    class Meta:
        abstract = True

class DeletableModelBase(models.Model):
    """
    This is an abstract Model used to provide
        delete, restore, purge, deleted_at and is_deleted()

    Its actually a misnomer because it allows an object to go into a deleted state
        but is never actually deleted
    """
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)


    @pre_and_post_signal
    def delete(self):
        self.deleted_at = datetime.now()
        self.save()

    def restore(self,*args,**kwargs):
        self.deleted_at = datetime.now()
        self.save()

    @pre_and_post_signal
    def purge(self,*args,**kwargs):
        super(DeletableModelBase,self).delete(*args,**kwargs)

    def is_deleted(self):
        return self.deleted_at != None
    
    class Meta:
        abstract = True


class CreatedByModelBase(models.Model):
    """
    This is an abstract Model used to provide
        created_by
        has_creator flag (which is used by CreatedByModelFormMixin)
    """
    created_by = models.ForeignKey(User, related_name='+', editable=False, blank=True, null=True)

    def has_creator(self):
        return not self.created_by==None
    
    class Meta:
        abstract = True
