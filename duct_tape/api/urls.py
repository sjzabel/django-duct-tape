from django.conf.urls.defaults import *
from duct_tape.api.handlers import BaseHandler, BaseAutoCompleteHandler
from duct_tape.api.handlers import BaseExtHandler
from piston.resource import Resource


class BaseGenericExtAPIEngine(object):
    # you will have to extend the view classes and then override these
    handler_klass = BaseExtHandler

    @classmethod
    def get_patterns(
            klass,
            model,
            app_path,
            alternate_url_prefix=None,
            fields=None,
            search_fields=None,
            **kwargs):

        model_name = model.__name__.lower() 
        if not app_path=="":
            app_path += ':'

        if not alternate_url_prefix:
            alternate_url_prefix = model_name

        app_path += alternate_url_prefix


        # Create Handler
        # Give this new form class a reasonable name.
        handler_class_name = model.__name__ + 'Handler'

        # Class attributes for the new form class.
        handler_class_attrs = {
                'model':model
        }
        if fields:
            handler_class_attrs['fields']=fields

        handler_class = type(handler_class_name, (klass.handler_klass,), handler_class_attrs)
        handler = Resource(handler_class)

        #TODO: figure out how you want to handle api/fis/fi
        return patterns('',
            (r'^%s/'%alternate_url_prefix,
                include(
                    patterns('',
                        url(r'^$', handler,  {'emitter_format': 'ext-json'}, name='list'),
                        url(r'^(?P<id>\d+)/$', handler, {'emitter_format': 'ext-json'}, name='show'),
                    ), namespace=alternate_url_prefix, app_name=alternate_url_prefix
                )
            ),
        )



class BaseGenericAPIEngine(object):
    # you will have to extend the view classes and then override these
    handler_klass = BaseHandler
    autocomplete_handler_klass = BaseAutoCompleteHandler

    @classmethod
    def get_patterns(
            klass,
            model,
            app_path,
            alternate_url_prefix=None,
            fields=None,
            search_fields=None,
            **kwargs):

        model_name = model.__name__.lower() 
        if not app_path=="":
            app_path += ':'

        if not alternate_url_prefix:
            alternate_url_prefix = model_name

        app_path += alternate_url_prefix


        # Create Handler
        # Give this new form class a reasonable name.
        handler_class_name = model.__name__ + 'Handler'

        # Class attributes for the new form class.
        handler_class_attrs = {
                'model':model
        }
        if fields:
            handler_class_attrs['fields']=fields

        handler_class = type(handler_class_name, (klass.handler_klass,), handler_class_attrs)
        handler = Resource(handler_class)

        # Create AutoCompleteHandler
        # Give this new form class a reasonable name.
        ac_handler_class_name = model.__name__ + 'AutoCompleteHandler'

        # Class attributes for the new form class.
        ac_handler_class_attrs = {}
        if search_fields:
            ac_handler_class_attrs['search_fields']=search_fields

        ac_handler_class = type(ac_handler_class_name, (handler_class, klass.autocomplete_handler_klass,), ac_handler_class_attrs)
        auto_complete_handler = Resource(ac_handler_class)

        return patterns('',
            (r'^%s/'%alternate_url_prefix,
                include(
                    patterns('',
                        url(r'^$', handler, name='list'),
                        url(r'^autocomplete/$', auto_complete_handler, name='autocomplete_list'),
                        url(r'^(?P<id>\d+)/$', handler, name='show'),
                    ), namespace=alternate_url_prefix, app_name=alternate_url_prefix
                )
            ),
        )
