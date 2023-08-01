from dependencies.registrator import add_factory_to_mapper
from services.views import ViewsService, ViewsServiceABC


@add_factory_to_mapper(ViewsServiceABC)
def create_views_service() -> ViewsService:
    return ViewsService()
