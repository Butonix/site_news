import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

def current_user_has_group(group):
    user = get_current_user()
    return group in [x.name for x in user.groups.all()]
    
class ThreadLocals(object):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
