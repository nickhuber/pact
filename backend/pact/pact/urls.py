from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import SimpleRouter

from pact import views as pact_views
from manager import views as manager_views
from roll import views as roll_views


router = SimpleRouter(trailing_slash=False)
router.register(
    r'characters/?',
    manager_views.CharacterViewSet,
)
router.register(
    r'encounters/?',
    manager_views.EncounterViewSet
)
router.register(
    r'encounter_characters/?',
    manager_views.EncounterCharacterViewSet
)
router.register(
    r'status_effects/?',
    manager_views.StatusEffectViewSet
)
router.register(
    r'users/?',
    pact_views.UserViewSet
)


admin.autodiscover()


urlpatterns = [
    url(
        r'^api/',
        include(router.urls)
    ),
    url(
        r'^api/admin/?',
        admin.site.urls
    ),
    url(
        r'^api/auth/?$',
        pact_views.LoginView.as_view(), name='authenticate'
    ),
    url(
        r'^api/register/?$',
        pact_views.RegisterView.as_view(), name='register'
    ),
    url(
        r'^api/roll/?$',
        roll_views.roll
    ),
]
