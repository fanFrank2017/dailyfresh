from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('df_user.urls')),
    url(r'^tinymce/',include('tinymce.urls')),
    url(r'^',include('df_goods.urls')),
    url(r'^cart/', include('df_cart.urls')),
]
