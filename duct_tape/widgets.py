from django.forms import widgets
from django.forms.util import flatatt
from django.utils import formats
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class ViewWidget(widgets.Widget):
    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            value = force_unicode(self._format_value(value))
        return mark_safe(u'<span %s >%s</span>' % (flatatt(final_attrs),value))

class ViewFKWidget(ViewWidget):
    def __init__(self,*args,**kwargs):
        if 'klass' in kwargs:
            self.klass = kwargs['klass']
            del kwargs['klass']

        super(ViewFKWidget,self).__init__(*args,**kwargs)

    def _format_value(self, value):
        if self.klass:
            value = self.klass.objects.get(pk=value)
            
        return value

class ViewTextWidget(widgets.Widget):
    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            value = force_unicode(self._format_value(value))
        return mark_safe(u'<blockquotes><span %s >%s</span></blockquotes>' % (flatatt(final_attrs),value))

