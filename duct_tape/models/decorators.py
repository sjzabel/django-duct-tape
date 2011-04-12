from django.dispatch import Signal
from functools import wraps

def register_pre_and_post_signal(klass,method_name):
    # create signals and expose in class
    method_names =[]
    if hasattr(method_name,'__iter__'):
        method_names = method_name

    else:
        method_names = [method_name]

    def _wrap(name,klass):
        pre_name = "pre_%s" % name
        post_name = "post_%s" % name

        setattr(klass,pre_name,Signal(providing_args=['instance']))
        setattr(klass,post_name,Signal(providing_args=['instance']))

        func = getattr(klass,name)

        @wraps(func)
        def _wrapper(self,*args,**kwargs):
            # send the pre signal
            for reciever,response in getattr(klass,pre_name).send(sender=klass, instance=self):
                if response == False:
                    #abort
                    return False
            # run the function    
            rslt = func(self,*args,**kwargs)
            
            # send the post signal
            getattr(klass,post_name).send(sender=klass, instance=self)

            return rslt

        setattr(klass,name,_wrapper)

    for name in method_names:
        _wrap(name,klass)
