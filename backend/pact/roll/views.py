from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pyparsing import ParseException

import dice


@api_view(http_method_names=['POST'])
def roll(request):
    if 'method' in request.data:
        if request.data['method'] == 'min':
            roller = dice.roll_min
        elif request.data['method'] == 'max':
            roller = dice.roll_max
        elif request.data['method'] == 'random':
            roller = dice.roll
        else:
            # Unsupported method
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        roller = dice.roll
    try:
        results = roller(request.data['query'])
    except (ParseException, KeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        # For some reason dice.roll will give us a list of the dice rolls
        # if asking for a single type, like "3d6" instead of "3d6 + 1"
        results = sum(results)
    except TypeError:
        pass

    return Response({'total': results})
