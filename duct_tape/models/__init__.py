from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_registry import UserRegistry


from duct_tape.models.decorators import register_pre_and_post_signal

from datetime import datetime

class DirtyModelMixin(object):
    '''
    Adds concept of *dirty* fields (ala, which fields changed)
    '''

    def __setattr__(self, name, value):
        for fld in self._meta.local_fields:
            if fld.name!=name:          continue
            if fld.rel:                 continue

            initial_value = None
            if name in self._modified_attrs:
                initial_value = self._modified_attrs[name]['initial_value']
            else:
                if hasattr(self, name):
                    initial_value = self.__getattribute__(name)

            if not initial_value:       continue
            if initial_value==value:    continue

            #checks complete
            if not self.is_dirty:
                self.is_dirty = True
            
            if name not in self._modified_attrs:
                self._modified_attrs[name] = {
                    'initial_value': initial_value
                }

            self._modified_attrs[name]['value'] = value

        super(DirtyModelMixin, self).__setattr__(name, value)

    def _reset_modified_attrs(self):
        self.is_dirty = False
        self._modified_attrs = {} 

    def __init__(self, *args, **kwargs):
        self._reset_modified_attrs()
        super(DirtyModelMixin, self).__init__(*args, **kwargs)

    def get_dirty_fields(self):
        return [(key, value) for key, value in self._modified_attrs.iteritems()]

class TimeStampedModelMixin(models.Model):
    """
    This is an abstract Model used to provide
        created_at
        updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    
    class Meta:
        abstract = True

class CreatedByModelMixin(object):
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
        kls = super(CreatedByModelMixin,klass).__new__(klass)
        if not klass in CreatedByModelMixin._class_signal_dict:
            dispatch_uid = "createdbymodelbase_auto_add_creator__%s.%s" % (klass.__module__, klass.__name__)

            # we don't need to keep the dispatch_uid around but it doesn't hurt
            CreatedByModelMixin._class_signal_dict[klass] = dispatch_uid

            post_save.connect(CreatedByModelMixin.auto_add_creator,sender=klass,weak=False,dispatch_uid=dispatch_uid)

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


class DeletableDeletedModelManager(models.Manager):
    def get_query_set(self):
        return super(DeletableDeletedModelManager,self
                ).get_query_set().exclude(deleted_at__isnull=True)

class DeletableNotDeletedModelManager(models.Manager):
    def get_query_set(self):
        return super(DeletableNotDeletedModelManager,self
                ).get_query_set().filter(deleted_at__isnull=True)

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
    
    #managers
    objects = DeletableNotDeletedModelManager()
    deleted_objects = DeletableDeletedModelManager()
    all_objects = models.Manager()
    
    class Meta:
        abstract = True


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

register_pre_and_post_signal(DeletableModelBase,['restore','delete'])

class StandardNamedUrlModelMixin(object):
    @models.permalink
    def get_absolute_url(self):
        return ('%s:%s:detail'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

    @models.permalink
    def get_absolute_detail(self):
        return ('%s:%s:detail'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

    @models.permalink
    def get_absolute_update(self):
        return ('%s:%s:update'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

    @models.permalink
    def get_absolute_new(self):
        return ('%s:%s:new'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

    @models.permalink
    def get_absolute_delete(self):
        return ('%s:%s:delete'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

    @models.permalink
    def get_absolute_list(self):
        return ('%s:%s:list'%(
            self.__class__._meta.app_label,
            self.__class__.__name__.lower()
            ),[str(self.id)])

