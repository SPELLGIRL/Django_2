from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse, urlparse
from django.core.files.base import ContentFile

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import CustomUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(
                              fields=','.join(
                                  ('bdate', 'sex', 'about', 'photo_max')),
                              access_token=response['access_token'],
                              v='5.92')), None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex'] and not user.customuserprofile.gender:
        user.customuserprofile.gender = CustomUserProfile.MALE if data[
                                                                      'sex'] == 2 else CustomUserProfile.FEMALE

    if data['about'] and not user.customuserprofile.aboutMe:
        user.customuserprofile.aboutMe = data['about']

    if data['photo_max'] and not user.avatar:
        image_url = data['photo_max']
        filename = urlparse(image_url).path.split('/')[-1]
        response = requests.get(image_url)
        user.avatar.save(filename,
                         ContentFile(response.content))

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    user.save()
