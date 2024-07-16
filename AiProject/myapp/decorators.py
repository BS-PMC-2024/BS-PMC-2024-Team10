

from django.shortcuts import render

def student_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_student:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return _wrapped_view_func

def practitioner_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_practitioner:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return _wrapped_view_func
