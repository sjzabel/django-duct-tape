from django.template import RequestContext as D_RequestContext
from duct_tape.lib.template_queue import TemplateQueue

class RequestContext(D_RequestContext):
    def __init__(self, request, dict=None,**kwargs):
        if not dict:
            dict = {}

        if not 'tab' in dict:
            dict['tab'] = None
        if not 'duct_tape__behavior_queue' in dict:
            dict['duct_tape__behavior_queue'] = TemplateQueue()
        
        super(RequestContext,self).__init__(request,dict=dict,**kwargs)
