# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy

from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog
from django.views.generic import RedirectView

last_modified_date = timezone.now()


#admin.autodiscover()
#admin.site.site_header = 'api.example.com'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/v1/', permanent=False)),
    url(r'^s/', include('social_django.urls', namespace='social')),
    url(r'^api/v1/', include('app.urls_api', namespace='api')),
]

urlpatterns += i18n_patterns(
    #url(r'^admin_tools/', include('admin_tools.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    #url('^account/', include('auth_extra.urls')),
    #url('^account/', include('django.contrib.auth.urls')),

    # url(r'^jsi18n/$',
    #     last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()),
    #     name='javascript-catalog'),

)

if settings.DEBUG:
    #urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static('/media/', document_root=settings.MEDIA_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
