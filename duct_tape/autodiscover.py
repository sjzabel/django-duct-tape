'''
this is an almost direct rip from contrib.admin.__init__
the only diff is the ability to choose the file to auto discover
'''
from django.contrib.admin.sites import site
import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

def autodiscover(module_name=None):
    """
    Auto-discover INSTALLED_APPS (module_name).py modules and fail silently when
    not present. This forces an import on them to register any (module_name) bits they
    may want.
    """
    print 'AUTODISCOVER'
    if not module_name: return False

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_s = '%s.%s' % (app,module_name)
            import_module(import_s)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, module_name):
                raise
