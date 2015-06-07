from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from roll import views as roll_views
from manager import views as manager_views


router = DefaultRouter(trailing_slash=False)
router.register('^characters', manager_views.CharacterViewSet)
router.register('^encounters', manager_views.EncounterViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
	url(r'^api/roll$', roll_views.roll),
]

urlpatterns += router.urls
