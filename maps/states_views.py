from states import CountStateMap, UniqueStateMap, FlatStateMap
from share.decorator import secret_key, no_share
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

def image_redirect(request, shared, display_user, type_):
    """ Redirect to the pre-rendered png image
    """
    if display_user.id == 1:
        display_user = None # unset user so it uses all users

    path = "%s/%s/%s" % (settings.SITE_URL,
                         settings.STATES_URL,
                         display_user.id)
    
    return HttpResponseRedirect("%s/states-%s.png" % (path, type_))

@secret_key
def render_all(request):
    from django.contrib.auth.models import User
    
    users = User.objects.order_by('id')
    
    for user in users:
        print user
        render_for_user(user)
        
    return HttpResponse('done!', mimetype="text/plain")


@no_share
@login_required
def render_me(request, shared, display_user):
    
    render_for_user(display_user)

    # return the user to their maps page with spiffy new updated images
    from django.core.urlresolvers import reverse
    url = reverse('maps', args=(display_user.username,) )

    return HttpResponseRedirect(url)


def render_for_user(user):
    """ Given a user instance, it renders the three map images and saves them
        into the appropriate directory.
    """
    import os
    
    BMP = settings.BASE_MAP_PATH
    
    #the directory that the images will be saved to
    directory = os.path.join(BMP, str(user.id))
    
    #if the directory is not there, then create it.
    if not os.path.isdir(directory):
        os.makedirs(directory)
        
    filename = os.path.join(directory, 'states-unique.png')
    f = open(filename, 'w')
    UniqueStateMap(user).to_file(f)
    f.close()
    
    filename = os.path.join(directory, 'states-count.png')
    f = open(filename, 'w')
    CountStateMap(user).to_file(f)
    f.close()
    
    filename = os.path.join(directory, 'states-colored.png')
    f = open(filename, 'w')
    FlatStateMap(user).to_file(f)
    f.close()