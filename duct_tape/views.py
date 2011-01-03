from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from duct_tape.lib.template_queue import TemplateQueue

class JSBehaviorQueueMixin(object):
    def get_context_data(self, **kwargs):
        context = super(JSBehaviorQueueMixin,self).get_context_data(**kwargs)

        # always create a behavior queue at the top level context
        context['duct_tape__behavior_queue'] = TemplateQueue()
        return context

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self,request, *args, **kwargs ):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
