from django.db import models

from djangoProject.utils.generl_model import BaseModel


# Create your models here.

class Banner(BaseModel):
    """轮播图模型"""
    title = models.CharField(max_length=40, verbose_name='广告标题')
    link = models.CharField(max_length=200, verbose_name='广告链接')
    image_url = models.ImageField(upload_to='banner', null=True, blank=True, max_length=255, verbose_name='轮播图像')
    re_mark = models.TextField(verbose_name='备注信息')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航栏"""
    POSITION_OPTION = (
        (1, '顶部导航'),
        (2, '尾部导航'),
    )
    title = models.CharField(max_length=40, verbose_name='导航标题')
    link = models.CharField(max_length=200, verbose_name='导航连接')
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name='导航栏位置')
    is_site = models.BooleanField(default=False, verbose_name='是否是站外地址')

    class Meta:
        db_table = "nav"
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
