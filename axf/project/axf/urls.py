from django.conf.urls import url
from. import views
urlpatterns = [
    url(r'^home/$', views.home, name="home"),
    # 使用在Mark后加了(\d+)匹配的时候就要进入Mark后加数字的网址中
    #而且一定要这样因为在 view中传了参数，在此两个不能共存
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name="market"),
    url(r'^cart/$', views.cart, name="cart"),



    url(r'^mine/$', views.mine, name="mine"),
    #登录
    url(r'^login/$',views.login, name="login"),
    #注册
    url(r'^register/$',views.register, name="register"),
    #验证账号是否被注册,  离焦的时候发起ajax请求  对这个页面checkuserid
    url(r'^checkuserid/$', views.checkuserid, name = "checkuserid"),
    #退出登录
    url(r'^quit/$', views.quit, name="quit"),
    #修改购物车
    url(r'^changecart/(\d+)/$', views.changecart, name="changecart"),
    url(r'^saveorder/$',views.saveorder, name="saveorder"),
]
