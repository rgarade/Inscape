from __future__ import absolute_import, unicode_literals    

import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import service

@api_view(['POST']) 
def mint_token(request):
    # logger.info("---End FUNCTION:checkCalendarSynced(request)/Views---")  
    try:  
        response = service.mintToken(10)
        return Response(response, status = status.HTTP_200_OK)
    except KeyError as e:
        response = {'Key Error' : str(e)}
        return Response(response, status = status.HTTP_400_BAD_REQUEST)
    finally:
        print("exit")
        # logger.info("---End FUNCTION:checkCalendarSynced(request)/Views---") 

