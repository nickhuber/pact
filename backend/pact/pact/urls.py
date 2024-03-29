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
router.register(
    r'pathfinder_monsters/?',
    manager_views.PathfinderMonsterViewSet
)
router.register(
    r'5e_monsters/?',
    manager_views.FifthEditionMonsterViewSet
)

admin.autodiscover()


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/admin/?', admin.site.urls),
    url(r'^api/auth/login/?$', pact_views.LoginView.as_view(), name='login'),
    url(r'^api/auth/logout/?$', pact_views.LogoutView.as_view(), name='logout'),
    url(r'^api/auth/register', pact_views.RegisterView.as_view(), name='register'),
    url(r'^api/roll/?$', roll_views.roll),
]
