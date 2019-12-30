from lib.http import render_json
from common.keys import VCODE_PREFIX

from django.core.cache import cache

# Create your views here.
from lib.sms import send_sms
from user.models import User


def user_phone(request):
    '''提交手机号，发送验证码'''
    phone = request.POST.get('phone')
    # phone = request.GET.get('phone')
    print(phone)
    send_sms(phone)
    return render_json(None)


def user_vcode(request):
    '''验证验证码'''
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    print(f'phone: {phone}')
    print(f'vcode: {vcode}')
    return render_json(verify_vcode(phone, vcode))


def verify_vcode(phone, vcode):
    # 取出缓存里保存的 vcode
    VCODE = VCODE_PREFIX
    server_vcode = cache.get(f'{VCODE}{phone}')
    print(server_vcode)
    print(f'server_vcode type:{type(server_vcode)}')
    print(f'vcode type:{type(vcode)}')

    # 比对两个 vocde 是否一致
    if str(server_vcode) == str(vcode):
        # 一致则让用户登录
        # get_or_create 返回的结构是一个 tuple，我们为了解包，用了 user, _
        user, _ = User.objects.get_or_create(phone=phone, nickname=phone)
        return user.to_dict()
    else:
        # 不一致则让用户重新登录:
        return {'vcode':10001}
