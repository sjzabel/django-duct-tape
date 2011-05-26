'''
Yanked from django, so that I could have a properly formatted message to use in a piston handler
'''

from piston.utils import rc

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from django.db.models import Q

import operator
from piston.handler import BaseHandler as PistonBaseHandler
def get_object_or_404(self,klass,*args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = klass.objects.all()
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        resp = rc.NOT_FOUND
        resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
        return resp

class BaseHandler(PistonBaseHandler):
    def get_object(self,*args, **kwargs):
        return get_object_or_404(self.model,*args,**kwargs)

    #TODO : name this something different and move the list making somewhere else
    def get_queryset(self, request, *args, **kwargs):
        """
        Uses filter() to return a list of objects, or raise a Http404 exception if
        the list is empty.

        """
        queryset = self.model.objects.all()
        if 'term' in request.GET:
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

                queryset = queryset.filter(reduce(operator.or_, or_queries))
                for field_name in self.search_fields:
                    if '__' in field_name:
                        queryset = queryset.distinct()
                        break

        if 'limit' in request.GET:
            print 'has limit'
            limit = 25
            if 'limit' in request.GET:
                limit = request.GET['limit']
            page = 1
            if 'page' in request.GET:
                print 'has page'
                page = int(request.GET['page'])

            end = limit * page

            start = 0
            if 'start' in request.GET:
                print 'has start'
                start = int(request.GET['start'])

            print limit
            print page
            print start
            queryset = queryset[start:end]

        return queryset


# helper baseclass

    def read(self,request,id=None):
        # on GET
        if id:
            return self.get_object(pk=id)
        else:
            queryset = self.get_queryset(request)
            obj_list = [obj for obj in queryset]
            if not obj_list:
                print "No Object List"
                resp = rc.NOT_FOUND
                resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
                return resp

            return obj_list      

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
        queryset = self.get_queryset(request)
        obj_list = [self.get_value_and_label(obj) for obj in queryset]
        return obj_list      

