from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter

from roll import views as roll_views
from manager import views as manager_views


router = SimpleRouter(trailing_slash=False)
router.register('characters', manager_views.CharacterViewSet)
router.register('encounters', manager_views.EncounterViewSet)
router.register('encounter_characters', manager_views.EncounterCharacterViewSet)


print router.urls
urlpatterns = [
    url(r'^api/roll$', roll_views.roll),
    url(r'^api/', include(router.urls)),
]
