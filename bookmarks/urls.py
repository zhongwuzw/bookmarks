from django.conf.urls import patterns, include, url
from bookmark.views import UserPage,HomePage,Logout,RegisterPage,BookMarksSavePage
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bookmarks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(\w+)/$',UserPage.as_view(),name = 'user_book_marks'),
    url(r'^login/$','django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^$',HomePage.as_view(),name = 'home_page'),
    url(r'^logout/$',Logout.as_view()),
    url(r'^register/$',RegisterPage.as_view()),
    url(r'^save/$',BookMarksSavePage.as_view()),
)
