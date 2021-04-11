"""
Заготовки типичных http ответов.
"""

from rest_framework import status as http_status
from rest_framework.response import Response


class ResponseOk:
    """HTTP_200_OK"""
    http_status = http_status.HTTP_200_OK
    status = True
    data_field_name = 'Data'

    def __new__(cls, details=None):
        """
        :type details: [Dict, str]
        """

        response = {'Status': cls.status}
        if isinstance(details, str):
            details = {'Description': details}
        response[cls.data_field_name] = details
        return Response(response, status=cls.http_status)


class ResponseCreated(ResponseOk):
    """HTTP_201_CREATED"""
    http_status = http_status.HTTP_201_CREATED


class ResponseDeleted(ResponseOk):
    """HTTP_204_NO_CONTENT"""

    # http_status = http_status.HTTP_204_NO_CONTENT

    def __new__(cls):
        return super().__new__(cls, {'Deleted': True})


class ResponseBadRequest(ResponseOk):
    """HTTP_400_BAD_REQUEST"""
    http_status = http_status.HTTP_400_BAD_REQUEST
    status = False
    data_field_name = 'Errors'


class ResponseForbidden(ResponseBadRequest):
    """HTTP_403_FORBIDDEN"""
    http_status = http_status.HTTP_403_FORBIDDEN


class ResponseConflict(ResponseBadRequest):
    """HTTP_409_CONFLICT"""
    http_status = http_status.HTTP_409_CONFLICT
    status = False


class ResponseNotFound(ResponseBadRequest):
    """HTTP_404_NOT_FOUND"""
    http_status = http_status.HTTP_404_NOT_FOUND
    status = False

    def __new__(cls):
        return super().__new__(cls, 'Not found')
