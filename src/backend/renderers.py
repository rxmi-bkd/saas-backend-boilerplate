from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success, is_redirect, is_informational, is_client_error, is_server_error


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code

        if is_informational(status_code):
            ...
        elif is_success(status_code):
            response = {
                'status': 'success',
                'data': data,
            }
        elif is_redirect(status_code):
            ...
        elif is_client_error(status_code):
            response = {
                'status': 'fail',
                'data': data,
            }
        elif is_server_error(status_code):
            ...

        return super(CustomJSONRenderer, self).render(response, accepted_media_type, renderer_context)
