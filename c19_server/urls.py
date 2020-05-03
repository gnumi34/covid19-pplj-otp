from django.urls import path, include
from rest_framework.routers import DefaultRouter
from c19_server.views import FormViewSet, UserIDViewSet, UserViewSet
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
userid_router = router.register('userids', UserIDViewSet, basename='userid')
userid_router.register('forms', FormViewSet, basename='userid-form',
                       parents_query_lookups=['userid'])
router.register('owner', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]