'''
provides a queue of strings or objs that can be coquerced into strings

provides ability to add unique key for templates that might appear multiple times
'''

class TemplateQueue(object):
    def __init__(self):
        self.dict = {}
        self.order_queue = []
        self.auto_key = 0

    def get_key(self):
        key = self.auto_key
        self.auto_key += 1
        return key

    def add_to_queue(self,s_or_obj,key=None):
        if not key:
            key = self.get_key()

        if not key in self.dict:
            self.dict[key]=s_or_obj # allows anything that can be coquerced into a string
            self.order_queue.append(key)

    def render(self):
        return self.__unicode__()

    def __unicode__(self):
        return ''.join([str(self.dict[key]) for key in self.order_queue])
