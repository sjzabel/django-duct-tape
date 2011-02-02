from django.forms import widgets
from django.forms.util import flatatt
from django.utils import formats
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from itertools import chain


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

class ViewFKWidget(widgets.Select):
    def __init__(self, attrs=None, choices=()):
        super(ViewFKWidget,self).__init__(attrs=attrs,choices=choices)
        self.selected_labels = []

    def render(self, name, value, attrs=None, choices=()):
        # print "---------------"
        # print "render"
        # print "---------------"
        # print name
        # print value
        # print attrs
        # print choices
        super(ViewFKWidget,self).render(name, value, attrs=attrs, choices=choices)
        # print output
        return ", ".join(self.selected_labels)

    def render_options(self, choices, selected_choices):
        selected_choices = set([force_unicode(v) for v in selected_choices])
        self.selected_labels = [label for v,label in chain(self.choices, choices) if force_unicode(v) in selected_choices]
        #print selected_choices
        return ""

    #def _format_value(self, value):
    #    if self.klass:
    #        value = self.klass.objects.get(pk=value)
    #        
    #    return value

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

