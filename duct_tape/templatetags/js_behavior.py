'''
{% behavior_queue key=paginate %}
  // js code
{% endbehavior_queue %}

{% render_behavior_queue %}
'''
from django import template
from duct_tape.lib.template_queue import TemplateQueue
register = template.Library()

@register.tag(name="behavior_queue")
def do_behavior_queue(parser,token):
    key = None 
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, key = token.split_contents()
    except ValueError:
        pass

    nodelist = parser.parse(('endbehavior_queue',))
    parser.delete_first_token()

    return BehaviorNode(nodelist,key)

class BehaviorNode(template.Node):
    def __init__(self, nodelist, key=None):
        self.key = key
        self.nodelist = nodelist

    def render(self, context):
        if not 'duct_tape__behavior_queue' in context:
            bq = TemplateQueue()
            context['duct_tape__behavior_queue'] = bq
        else:
            bq = context['duct_tape__behavior_queue']

        bq.add_to_queue(self.nodelist.render(context),self.key)
        
        context['duct_tape__behavior_queue'] = bq
        return '' 

@register.tag(name="render_behavior_queue")
def do_render_behavior_queue(parser,token):
    return RenderBehaviorNode()

class RenderBehaviorNode(template.Node):
    def render(self,context):
        if not 'duct_tape__behavior_queue' in context:
            return ''
        else:
            return '''
<script>
$(function(){
    %s
});
</script>
''' % context['duct_tape__behavior_queue'].render()

