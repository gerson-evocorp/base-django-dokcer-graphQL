# https://gist.githubusercontent.com/smmoosavi/033deffe834e6417ed6bb55188a05c88/raw/3393e415f9654f849a89d7e33cfcacaff0372cdd/views.py
import traceback

from django.conf import settings
from graphql.error import GraphQLSyntaxError
from graphql.error.located_error import GraphQLLocatedError
from graphql.error import GraphQLError
from graphql.error import format_error as format_graphql_error
from ..exceptions import ResponseError
from ..str_converters import to_kebab_case, dict_key_to_camel_case
from django.http import HttpResponse
from rest_framework.exceptions import APIException 
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from graphene_django.views import GraphQLView


def encode_code(code):
    if code is None:
        return None
    return to_kebab_case(code)


def encode_params(params):
    if params is None:
        return None
    return dict_key_to_camel_case(params)


def format_response_error(error: ResponseError):
    return {
        'message': error.message,
        'code': encode_code(error.code),
        'params': encode_params(error.params),
    }


def format_internal_error(error: Exception):
    message = 'Internal server error'
    code = 'internal-server-error'
    if settings.DEBUG:
        params = {
            'exception': type(error).__name__,
            'message': str(error),
            'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
        }
        return {
            'code': code,
            'message': message,
            'params': params,
        }
    return {
        'code': code,
        'message': message,
    }


def format_located_error(error):
    if isinstance(error.original_error, GraphQLLocatedError):
        return format_located_error(error.original_error)
    if isinstance(error.original_error, ResponseError):
        return format_response_error(error.original_error)
    return format_internal_error(error.original_error)


class SafeGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        data = {
            'message': str(error),
        }

        if isinstance(error, GraphQLLocatedError):
            print("\n\n\nGraphQLLocatedError\n\n\n")
            data.update(format_graphql_error(error))
            if isinstance(error.original_error, Exception):
                error = error.original_error
            else:
                return data

        if isinstance(error, APIException):
            print("\n\n\nAPIException\n\n\n")
            if isinstance(error, ValidationError):
                data.update({
                    'message': _('Validation error'),
                    'code': 'validation_error',
                    'fields': error.detail
                })
            else:
                if getattr(error, 'error_code', None):
                    data['code'] = error.error_code

                if getattr(error, 'extra', None):
                    data.update(error.extra)

        # elif isinstance(error, DjangoPermissionDenied):
        #     data.update({
        #         'message': _('Permission denied'),
        #         'code': 'permission_denied'
        #     })

        elif isinstance(error, GraphQLError):
            print("\n\n\nGraphQLError\n\n\n")
            help(error)
            data.update({
                'message': 'Ocorreu uma falha durante esta operação. Por favor verifique se está tudo certo. Se o problema persistir entre em contato com o suporte!',
                'code': 'validation_error',
                'extensions': str(error.extensions),
                'locations': str(error.locations),
                'nodes': str(error.nodes),
                'path': str(error.path),
                'positions': str(error.positions),
                'message_base': str(error.message),
            })             

        # elif isinstance(error, HttpError):
        #     print("\n\n\nHttpError\n\n\n")
            # pass

        else:
            data['code'] = 'unhandled_exception'
            if not settings.DEBUG:
                data['message'] = _('Server error')
            else:
                # data['message'] = '{}: {}'.format(error.__class__.__name__, error)
                data['message'] = "Erro interno"
                # data['traceback'] = itertools.chain(
                #     *[[l for l in ll.split('\n') if l.strip() != '']
                #     for ll in traceback.format_exception(
                #         error.__class__, error, error.__traceback__)])

        return data