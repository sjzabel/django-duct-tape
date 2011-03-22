'''
Yanked from django, so that I could have a properly formatted message to use in a piston handler
'''

from piston.utils import rc

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from django.db.models import Q

import operator

def _get_queryset(klass):
    """
    Returns a QuerySet from a Model, Manager, or QuerySet. Created to make
    get_object_or_404 and get_list_or_404 more DRY.
    """
    if isinstance(klass, QuerySet):
        return klass
    elif isinstance(klass, Manager):
        manager = klass
    else:
        manager = klass._default_manager
    return manager.all()

def get_object_or_404(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        resp = rc.NOT_FOUND
        resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
        return resp

def get_list_or_404(klass, *args, **kwargs):
    """
    Uses filter() to return a list of objects, or raise a Http404 exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        resp = rc.NOT_FOUND
        resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
        return resp

    return obj_list      

# helper baseclass

from piston.handler import BaseHandler as PistonBaseHandler

class BaseHandler(PistonBaseHandler):
    def read(self,request,id=None):
        # on GET
        if id:
            return get_object_or_404(self.model,pk=id)
        else:
            return self.model.objects.all()

    def create(self,request,*args,**kwargs):
        return super(BaseHandler,self).create(request,*args,**kwargs)

    def update(self,request,*args,**kwargs):
        # on PUT
        return super(BaseHandler,self).update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        # on DELETE
        return super(BaseHandler,self).delete(request,*args,**kwargs)

class BaseAutoCompleterHandler(BaseHandler):
    search_fields = None
    
    def get_value_and_label(self,obj):
        return {'label':str(obj),
                 'value':obj.pk}

    def read(self,request):
        qs = super(BaseAutoCompleterHandler,self).read(request)
        term = request.GET['term']

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        if self.__class__.search_fields:
            or_queries = [Q(**{construct_search(str(field_name)): term}) for field_name in self.search_fields]

            qs = qs.filter(reduce(operator.or_, or_queries))
            for field_name in self.search_fields:
                if '__' in field_name:
                    qs = qs.distinct()
                    break

        rows = [self.get_value_and_label(obj) for obj in qs]

        return rows

