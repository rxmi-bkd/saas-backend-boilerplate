from .views import QRCodeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', QRCodeViewSet)

urlpatterns = router.urls
