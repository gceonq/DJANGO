from django.conf.urls import url,include
from  testapp import views
#from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm,password_reset_complete
urlpatterns = [
    url(r'^$',views.baseview,name='base'),
    url(r'^login/$',views.loginview,name='login'),
    url(r'^register/$',views.register,name='register'),
    #url(r'^activateview/(?P<pk>\d+)/$', views.activate_view, name='activate_view'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^profile/$',views.view_profile,name='view_profile'),
    url(r'^edit/$',views.edit_profile,name='edit_profile'),
    url(r'^changepassword/$',views.change_password,name='change_password'),


    #url(r'^reset-password/$',password_reset,name='reset_password '),
   # url(r'^reset-password/done/$', password_reset_done, name='reset_password_done '),
    #url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='reset_password_confirm '),
   # url(r'^reset-password/complete/$', password_reset_complete, name='reset_password_complete '),

    url(r'^password/$', views.password_info, name='password_info'),



]