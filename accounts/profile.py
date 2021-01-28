# accounts.profile.py

from order.models import BaseOrderInfo
from accounts.forms import CustomerSignUpForm


def retrieve(request):
    """ gets the UserProfile instance for a user, creates one if it does not exist """
    try:
        profile = request.user.get_profile()
    except BaseOrderInfo.DoesNotExist:
        profile = BaseOrderInfo(user=request.user)
        profile.save()
    return profile

    
def set(request):
    """ updates the information stored in the user's profile """
    profile = retrieve(request)
    profile_form = CustomerSignUpForm(request.POST, instance=profile)
    profile_form.save()
    