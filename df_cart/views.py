# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *
from df_user import user_decorator

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车','sub_page_name':1,
               'carts':carts}
    return render(request,'df_cart/cart.html',context)