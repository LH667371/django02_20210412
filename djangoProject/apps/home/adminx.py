import xadmin
from xadmin import views

from home.models import Banner, Nav


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin 全局配置"""
    site_title = "百知学城"  # 设置站点标题
    site_footer = "百知教育科技有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


# 将轮播图模型注册到后台
class BannerModelAdmin(object):
    list_display = ['id', "title", 'link', "orders", "is_show"]
    ordering = ['id']


xadmin.site.register(Banner, BannerModelAdmin)


class NavModelAdmin(object):
    list_display = ['id', "title", "link", "position", "is_show"]
    ordering = ['id']


xadmin.site.register(Nav, NavModelAdmin)