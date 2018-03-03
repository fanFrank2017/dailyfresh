#coding=utf-8

from django.shortcuts import render,redirect,HttpResponseRedirect
from models import *
from df_goods.models import GoodsInfo
from hashlib import sha1
from django.http import JsonResponse,HttpResponse
from . import user_decorator

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码是否相同
    if upwd!=upwd2:
        #使用重定向，重新加载register页面
        return redirect('/user/register/')
    #如果密码相同，就进行密码加密，使用哈希sha1加密
    s1 = sha1() #创建对象
    s1.update(upwd)
    upwd3 = s1.hexdigest() #hexdigest为40位长度

    #如果密码相同，创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save() #保存到数据库中
    return redirect('/user/login/') #注册成功，转到登录页面

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0) #从表单接收数据，若jizhu是空，则默认值为0
    #根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    print uname
    #判断：如果未查到用户名错，则判断是否密码正确，正确则转到用户中心
    if len(users)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            #记住用户名
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
                #设置cookie信息，max_age为60，则有效期是60s，若为-1，则cookie立马过期
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            #说明是密码错误，所以error_pwd返回1，显示红色错误提示信息
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        #说明是用户名错误，所以error_name返回1，显示红色错误提示信息
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):
    #从login中获取到request.session的id，再从数据库中查询email
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览的设置
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for goods_id in goods_ids1:
        goods_list.append( GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title':'用户中心',
               'user_name':request.session['user_name'],
               'user_email':user_email,
               'info':1,
               'sub_page_name':1,
               'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context = {'title':'用户中心',
               'order':1,
               'sub_page_name': 1}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    #从数据库查询数据，发送给页面进行显示
    user = UserInfo.objects.get(id=request.session['user_id'])
    #如果用户在页面更改地址信息，页面是用post发送jc进行修改
    if request.method=='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心',
               'user':user,
               'site':1,
               'sub_page_name': 1}
    return render(request,'df_user/user_center_site.html',context)