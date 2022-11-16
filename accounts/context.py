# accounts.context.py


def profile(request):
    return {"profile": request.user}
