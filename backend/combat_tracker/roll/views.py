from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pyparsing import ParseException

import dice


@api_view(http_method_names=['POST'])
def roll(request):
    try:
        results = dice.roll(request.data['query'])
    except (ParseException, KeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        # For some reason dice.roll will give us a list of the dice rolls
        # if asking for a single type, like "3d6" instead of "3d6 + 1"
        results = sum(results)
    except TypeError:
        pass

    return Response({'total': results})
