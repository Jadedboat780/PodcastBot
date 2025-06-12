from .errors import router as error_router
from .start_dialogue import router as start_router
from .support import router as support_router
from .url import router as url_router

handlers = (start_router, support_router, url_router, error_router)
