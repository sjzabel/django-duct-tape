from piston.emitters import Emitter
import logging
log = logging.getLogger('console.debug')

class CSVEmitter(Emitter):
    def render(self,request):
        rows = self.construct()
        return "\n".join([
            ','.join([str(col) for col in row]) for row in rows])
#Emitter registered in duct_tape/__init__.py
from django.utils import simplejson
from django.core.serializers.json import DateTimeAwareJSONEncoder

class ExtJSONEmitter(Emitter):
    """
    JSON emitter, understands timestamps, wraps result set in object literal
    for Ext JS compatibility
    """
    def render(self, request):
        cb = request.GET.get('callback')

        totalCount = False
        if hasattr(self,'data') and hasattr(self.data,'__len__') and len(self.data)==2:
           totalCount,self.data= self.data
        ext_dict = {'success': True, 'data': self.construct()}
        if totalCount:
            ext_dict['totalCount'] = totalCount

        seria = simplejson.dumps(
                ext_dict, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)

        # Callback
        if cb:
            return '%s(%s)' % (cb, seria)

        return seria

#Emitter registered in duct_tape/__init__.py
