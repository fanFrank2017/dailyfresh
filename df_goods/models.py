#coding=utf-8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    #定义商品分类显示的title
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        #为了防止ttitle返回中文报ascii错误，添加encode（‘utf-8’）
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    #定义图片变量，在df_goods中加载，同时到setting.py中指定路径
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')
    #点击量
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200) #商品简介
    gkucun = models.IntegerField() #库存
    #使用HTML编辑器，将商品详情编辑交给用户，支持用户多样的内容
    gcontent = HTMLField() #需在setting.py中添加tinymce应用
    gtype = models.ForeignKey(TypeInfo)
    #推荐变量，或者是广告变量
    gadv = models.BooleanField(default=False)
    def __srt__(self):
        return self.gtitle.encode('utf-8')