from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from duct_tape.lib.template_queue import TemplateQueue
from anyjson import deserialize

class JSBehaviorQueueMixin(object):
    def get_context_data(self, **kwargs):
        context = super(JSBehaviorQueueMixin,self).get_context_data(**kwargs)

        # always create a behavior queue at the top level context
        context['duct_tape__behavior_queue'] = TemplateQueue()
        return context

class ModelUrlPathMixin(object):
    # this is needed because the base generic view class introspects in on itself
    # to insure that it is only receiving params that already exist in it
    url_list_path='list'
    url_detail_path='detail'
    url_update_path='update'
    url_delete_path='delete'
    url_create_path='create'
    url_api_autocomplete_path='api:foo:autocomplete_list'

    def get_context_data(self, **kwargs):
        context = super(ModelUrlPathMixin,self).get_context_data(**kwargs)

        context['url_list_path'] = self.url_list_path
        context['url_detail_path'] = self.url_detail_path
        context['url_update_path'] = self.url_update_path
        context['url_delete_path'] = self.url_delete_path
        context['url_create_path'] = self.url_create_path
        context['url_api_autocomplete_path'] = self.url_api_autocomplete_path

        return context


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self,request, *args, **kwargs ):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class NamedUrlDeletionMixin(object):
    '''
    This mixin trys reverse on the success_url
    and falls back to the original method if there is no success
    '''
    def get_success_url(self):
        if self.success_url:
            url = reverse(self.success_url)
            if url:
                return url
            else:
                return super(NamedUrlDeletionMixin,self).get_success_url()
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

class MultipleObjectFilterMixin(object):
    '''
    Used to provide generic list views a way of filtering

    Provides a mechanism for passing a filter_string through the request
    '''

    def get_queryset(self,*args,**kwargs):
        super(MultipleObjectFilterMixin,self).get_queryset(*args,**kwargs)
        qs = self.queryset
        if 'filter' in self.request.GET:
            data = deserialize(self.request.GET['filter'])
            qs=qs.filter(**data)
        return qs.all()
