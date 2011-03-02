from django.forms import widgets
from django.forms.util import flatatt
from django.utils import formats
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from itertools import chain
from django.core.urlresolvers import reverse

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

class ViewURLWidget(widgets.Widget):
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
        return mark_safe(u'<span %s ><a href="%s">%s</a></span>' % (flatatt(final_attrs),value,value))

class ViewFKWidget(widgets.Select):
    def __init__(self, attrs=None, choices=(),url_path=None):
        super(ViewFKWidget,self).__init__(attrs=attrs,choices=choices)
        self.selected_labels = []
        self.url_path = url_path


    def _format(self,v,label):
        if self.url_path and v != '':
            return "<a href='%s'>%s</a>"%(reverse(self.url_path,args=[v]),label)
        else:
            return label

    def render(self, name, value, attrs=None, choices=()):
        super(ViewFKWidget,self).render(name, value, attrs=attrs, choices=choices)
        # print output
        return mark_safe(u", ".join(self.selected_labels))

    def render_options(self, choices, selected_choices):
        selected_choices = set([force_unicode(v) for v in selected_choices])
        self.selected_labels = [self._format(v,label) for v,label in chain(self.choices, choices) if force_unicode(v) in selected_choices]
        #print selected_choices
        return ""


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

