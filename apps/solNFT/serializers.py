from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    createdby = serializers.CharField(
        source='iCreatedBy.sFirstName', read_only=True)
    modifiedby = serializers.CharField(
        source='iModifiedBy.sFirstName', read_only=True)
    print("data", createdby)

    class Meta:
        model = User
        fields = ['pk', 'sFirstName', 'sLastName', 'sAddressLine1', 'sAddressLine2', 'sCity', 'iZipCode', 'sEmailaddress',
                  'iPhoneNumber', 'sWalletAddress', 'dDOB', 'iCountryCode', 'sStatus', 'createdby', 'modifiedby', 'dCreatedDate', 'dModifiedDate']


class propertySerializer(serializers.ModelSerializer):
    # PropertyCatogary = serializers.CharField(source='ePropertyCategoryId', read_only=True)
    PropCreatedBy = serializers.CharField(
        source='iCreatedBy.sFirstName', read_only=True)
    PropModifiedBy = serializers.CharField(
        source='iCreatedBy.sFirstName', read_only=True)
    Currency = serializers.CharField(
        source='iCurrencyId.sCurrencyName', read_only=True)

    class Meta:
        model = PropertyMaster
        fields = ["sPropertyName", "ePropertyCategoryId","sPropertyDesc", "sPropertyAddressLine1", "sPropertyAddressLine2", "sCity", "iZipCode", "bLegalClearance", "bTechnicalClearance", "sAvailabilityStatus", "dAvailabilityDate",
                  "sPropertyPhotos", "sPropertyDocs", "fPropertyCurrentPrice", "Currency","iCurrencyId", "PropCreatedBy", "dCreatedDate", "PropModifiedBy", "dModifiedDate", "bLogicalDelete"]



class currencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyMaster
        fields = ['pk', 'sCurrencyName']



class UserPropertySerializer(serializers.ModelSerializer):
    createdby = serializers.CharField(
        source='iCreatedBy.sFirstName', read_only=True)
    modifiedby = serializers.CharField(
        source='iModifiedBy.sFirstName', read_only=True)
    PropertyName = serializers.CharField(
        source='iPropertyId.sPropertyName', read_only=True)
    TransactionUserId = serializers.CharField(
        source='iTransactionUserId.sFirstName', read_only=True)
    Description = serializers.CharField(
        source='iPropertyId.sPropertyDesc', read_only=True)
    CurrencyName = serializers.CharField(
        source='iCurrencyId.sCurrencyName', read_only=True)
    class Meta:
        model = User
        fields = ['pk','iPropertyId','PropertyName','Description','dStartDate', 'dEndDate', 'eTypeofTimeshare', 'eTypeofTransaction', 'iTransactionUserId','TransactionUserId', 'fTransactionAmount', 'fTransactionFee',
                  'iCurrencyId','CurrencyName','sJSONObject','createdby','modifiedby','dCreatedDate','dModifiedDate']

