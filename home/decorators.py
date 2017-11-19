from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


def custom_login_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            messages.add_message(request, messages.WARNING, "Sorry, You need to login to view this page.")
            return decorated_view_func(request, redirect_field_name='next')  # return redirect to signin

        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


@decorator_with_arguments
def custom_permission_required(function, perm, message_type, message):
    def _function(request, *args, **kwargs):
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, message_type, message)
            return redirect('index')
            # Return a response or redirect to referrer or some page of your choice

    return _function
