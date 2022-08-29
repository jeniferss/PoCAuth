from mcoloredlogger.functions import setup_logger
from django.utils.deprecation import MiddlewareMixin


class HTTPLoggerMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        logger = setup_logger()
        logger.http(f'{request.META.get("REMOTE_ADDR")} {request.method} {request.META.get("PATH_INFO")}', {"status": response.status_code})

        return response
