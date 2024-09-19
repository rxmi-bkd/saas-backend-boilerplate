from rest_framework.renderers import JSONRenderer
from rest_framework.status import (is_client_error, is_informational, is_redirect, is_server_error, is_success)


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code

        if is_informational(status_code):
            response = {'status': 'info', 'data': data, }
        elif is_success(status_code):
            response = {'status': 'success', 'data': data, }
        elif is_redirect(status_code):
            response = {'status': 'redirect', 'data': data, }
        elif is_client_error(status_code):
            response = {'status': 'fail', 'data': data, }
        elif is_server_error(status_code):
            response = {'status': 'error', 'message': data, }

        return super(CustomJSONRenderer, self).render(response, accepted_media_type, renderer_context)
