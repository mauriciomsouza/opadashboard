from django.conf.urls import include, url
from django.contrib import admin

from mano_id import urls as mano_id_urls
from homesite.views import HomeSiteView

urlpatterns = [
    url(r'', include(mano_id_urls, namespace='mano_id')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeSiteView.as_view(), name="home"),
]
