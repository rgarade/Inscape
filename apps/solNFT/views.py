from __future__ import absolute_import, unicode_literals

import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import service
from Inscape.__init__ import logger


@api_view(['POST'])
def mint_token(request):
    logger.info("---Start FUNCTION:mint_token(request)/Views---")
    try:
        response = service.mintToken(10)
        return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    finally:
        print("exit")
        logger.info("---End FUNCTION:mint_token(request)/Views---")


@api_view(['POST'])
def login(request):
    logger.info("---End FUNCTION:login(request)/Views---")
    try:
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        response = service.login(username, password)
        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    finally:
        logger.info("---End FUNCTION:login(request)/Views---")


@api_view(['GET'])
def logout(request):
    logger.info("---End FUNCTION:logout(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.logout(authToken)
        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def saveUserDetails(request):
    logger.info("---End FUNCTION:saveUserDetails(request)/Views---")
    try:
        body = json.loads(request.body)
        response = service.saveUserDetails(body)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserDetails(request):
    logger.info("---End FUNCTION:getUserDetails(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_property(request):
    logger.info("---End FUNCTION:getAllProperty(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = service.getAllProperty()
            return Response(response, status=status.HTTP_200_OK)

    except KeyError as e:
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    finally:
        logger.info("---End FUNCTION:getAllProperty(request)/Views---")


@api_view(['GET'])
def get_all_property_filtered(request):
    logger.info("---End FUNCTION:getAllPropertyFilterd(request)/Views---")
    try:
        body = json.loads(request.body)
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = service.getAllPropertyFiltered(body)
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_property_details(request):
    logger.info("---End FUNCTION:getPropertyDetails(request)/Views---")
    try:
        body = json.loads(request.body)
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = service.getPropertyDetails(body)
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserDetails : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_currency(request):
    logger.info("---End FUNCTION:getAllCurrency(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = service.getAllCurrency()
            return Response(response, status=status.HTTP_200_OK)

    except KeyError as e:
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    finally:
        logger.info("---End FUNCTION:getAllProperty(request)/Views---")



@api_view(['GET'])
def get_account_info(request):
    logger.info("---End FUNCTION:getAccountInfo(request)/Views---")
    try:
        body = json.loads(request.body)
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserDetails(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = service.getAccountInfo(body)
            return Response(response, status=status.HTTP_200_OK)

    except KeyError as e:
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    finally:
        logger.info("---End FUNCTION:getAllProperty(request)/Views---")

@api_view(['GET'])
def getUserOwnedProperty(request):
    logger.info("---End FUNCTION:getUserOwnedProperty(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserOwnedProperty(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserOwnedProperty : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUserListedProperty(request):
    logger.info("---End FUNCTION:getUserListedProperty(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserListedProperty(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserListedProperty : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUserSellProperty(request):
    logger.info("---End FUNCTION:getUserSellProperty(request)/Views---")
    try:
        authToken = request.META['HTTP_AUTHORIZATION']
        response = service.getUserSellProperty(authToken)

        if(response["status"] == False):
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        logger.error(f"Key Error in getUserSellProperty : {e}")
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)