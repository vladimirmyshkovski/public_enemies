from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from public_enemies.enemies import views

urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    #url(r'^$', include('enemies.urls', namespace='enemies')),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<enemy_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^добавить/$', views.CreateView.as_view(), name='create'),
    url(r'^казнить/(?P<enemy_id>[0-9]+)/$', views.UpVoteView.as_view(), name='downvote'),
    url(r'^помиловать/(?P<enemy_id>[0-9]+)/$', views.DownVoteView.as_view(), name='upvote'),
    url(r'^комментарии/', include('fluent_comments.urls')),
    #url(r'^draceditor/', include('draceditor.urls')),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    #url(r'^users/', include('public_enemies.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
