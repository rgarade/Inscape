from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    createdby = serializers.CharField(source='iCreatedBy.sFirstName', read_only=True)
    modifiedby = serializers.CharField(source='iModifiedBy.sFirstName', read_only=True)
    print("data",createdby)
    class Meta:
        model = User
        fields = ['pk', 'sFirstName', 'sLastName', 'sAddressLine1', 'sAddressLine2', 'sCity', 'iZipCode', 'sEmailaddress', 'iPhoneNumber', 'sWalletAddress','dDOB','iCountryCode','sStatus','createdby','modifiedby','dCreatedDate','dModifiedDate']