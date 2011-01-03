class UserRegistryRegisterError(Exception):
    ''' There is already a user in the registry '''
    pass

class UserRegistryUnregisterError(Exception):
    ''' There is no user in the registry '''
    pass

class UserRegistryUnregisterWrongUserError(Exception):
    ''' There is no user in the registry '''
    pass

class UserRegistry(object):
    '''
    singleton object to hold on to the request user
    for use in models & signals

    doing this for a wsgi stack... no idea of how it would work in a multithreaded environment

    note: maybe allow Anon Users
    note: maybe allow for Default System User
    '''
    _user = None

    @classmethod
    def register(klass,user):
        '''
        _user should always None else raise error
        '''
        if klass._user:
            raise UserRegistryRegisterError()

        klass._user = user

    @classmethod
    def unregister(klass,user):
        '''
        _user should not be None else raise error
        '''
        if not klass._user:
            raise UserRegistryUnregisterError()

        if not klass._user == user:
            raise UserRegistryUnregisterWrongUserError()

        klass._user = None

    @classmethod
    def has_user(klass):
        return klass._user != None
        
    @classmethod
    def get_user(klass):
        return klass._user

class UserRegistryMiddleware(object):
    def process_request(self, request):
        print "UserRegistryMiddleware - process_request"
        user = self.get_user(request)
        if user:
            UserRegistry.register(user)

    
    def process_response(self, request, response):
        print "UserRegistryMiddleware - process_response"
        user = self.get_user(request)
        if user:
            UserRegistry.unregister(user)

        return response
    
    def get_user(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            return request.user
        else:
            return None



