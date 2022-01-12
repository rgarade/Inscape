from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
# import jsonfield
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    email = None
    first_name = None
    last_name = None
    password = None
    is_active = None
    date_joined = None
    last_login = None
    
    sFirstName = models.CharField(max_length=50, unique=False,blank=True, null= False)
    sLastName = models.CharField(max_length=50, unique=False,blank=True, null= False)
    sAddressLine1 = models.CharField(max_length=500, unique=False,blank=True, null= False)
    sAddressLine2 = models.CharField(max_length=500, unique=False,blank=True, null= True)
    sCity = models.CharField(max_length=100, unique=False,blank=True, null= False)
    iZipCode = models.IntegerField(unique=False, blank=True, null= False)
    iStateid = models.ForeignKey('StateMaster', on_delete=models.CASCADE,related_name='user_state_id',blank=True, null= True)
    iCountryid = models.ForeignKey('CountryMaster', on_delete=models.CASCADE,related_name='user_country_id',blank=True, null= True)
    sEmailaddress = models.EmailField(max_length = 254)
    sPassword = models.CharField(max_length=100, unique=False,blank=True, null= False)
    iPhoneNumber = models.IntegerField(unique=False, blank=True, null= False)
    sWalletAddress = models.CharField(max_length=250, unique=False,blank=True, null= False)
    dDOB = models.DateField(blank=True, null= False)
    sStatus = models.CharField(max_length=50, unique=False,blank=True, null= False,default='Active')
    iCreatedBy = models.ForeignKey('self', on_delete=models.CASCADE,related_name='user_created_by',blank=True, null= True)
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey('self', on_delete=models.CASCADE,related_name='user_modified_by',blank=True, null= True)
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False,default=False)

    class Meta:
        db_table = 'tblUserMaster'

class CurrencyMaster(models.Model):
    sCurrencyName = models.CharField(max_length=100, unique=False,blank=True, null= False)
    iCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='currency_created_by')
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='currency_modified_by')
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False)

    class Meta:
        db_table = 'tblCurrencyMaster'



class PropertyMaster(models.Model):
    class PropertyCategory(models.TextChoices):
        East = 'E', _('East')
        West = 'W', _('West')
        South = 'S', _('South')
        North = 'N', _('North')
    sPropertyName = models.CharField(max_length=350, unique=False,blank=True, null= False)
    sPropertyDesc = models.CharField(max_length=2000, unique=False,blank=True, null= False)
    sPropertyAddressLine1 = models.CharField(max_length=1000, unique=False,blank=True, null= False)
    sPropertyAddressLine2 = models.CharField(max_length=1000, unique=False,blank=True, null= False)
    sCity = models.CharField(max_length=50, unique=False,blank=True, null= False)
    iZipCode = models.IntegerField(unique=False, blank=True, null= False)
    iStateid = models.ForeignKey('StateMaster', on_delete=models.CASCADE,related_name='property_state_id')
    iCountryid = models.ForeignKey('CountryMaster', on_delete=models.CASCADE,related_name='property_country_id')
    bLegalClearance = models.BooleanField(unique=False, blank=True, null= False)
    bTechnicalClearance = models.BooleanField(unique=False, blank=True, null= False)
    sAvailabilityStatus = models.CharField(max_length=50, unique=False,blank=True, null= False)
    dAvailabilityDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    sPropertyPhotos = models.CharField(max_length=50, unique=False,blank=True, null= False)
    sPropertyDocs = models.CharField(max_length=50, unique=False,blank=True, null= False)
    fPropertyCurrentPrice = models.FloatField(unique=False,blank=True, null= True)
    iCurrencyId = models.ForeignKey(CurrencyMaster, on_delete=models.CASCADE,related_name='property_currency_id')
    ePropertyCategoryId = models.CharField(max_length=100,choices=PropertyCategory.choices)
    iLatitude = models.IntegerField(unique=False, blank=True, null= False)
    iLongitude = models.IntegerField(unique=False, blank=True, null= False)
    fLandArea = models.FloatField(unique=False,blank=True, null= True)
    fLivingArea = models.FloatField(unique=False,blank=True, null= True)
    LegalDocumentsURL = models.CharField(max_length=1000, unique=False,blank=True, null= False)
    TechicalDocumentsURL = models.CharField(max_length=1000, unique=False,blank=True, null= False)
    sDeedtype = models.CharField(max_length=500, unique=False,blank=True, null= False)
    sFireplace = models.CharField(max_length=500, unique=False,blank=True, null= False)
    iNoofParkings = models.IntegerField(unique=False, blank=True, null= False)
    iNoofFloors = models.IntegerField(unique=False, blank=True, null= False)
    iNoofGarages = models.IntegerField(unique=False, blank=True, null= False)
    iApproxAge = models.IntegerField(unique=False, blank=True, null= False)
    fPropTax = models.FloatField(unique=False,blank=True, null= True)
    sConstructionSstyle = models.CharField(max_length=500, unique=False,blank=True, null= False)
    iCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='property_created_by')
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='property_modified_by')
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False)

    class Meta:
        db_table = 'tblPropertyMaster'



class UserProperty(models.Model):
    class TypeofTimeshare(models.TextChoices):
        Fixed_Week = 'fixed', _('Fixed Week')
        Floating_Week = 'floating', _('Floating Week')

    class TypeofTransaction(models.TextChoices):
        
        Buy = 'B', _('Buy')
        Sell = 'S', _('Sell')
        List = 'L',_('List')

    iUserId = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userProperty_user_id')
    iPropertyId = models.ForeignKey(PropertyMaster, on_delete=models.CASCADE,related_name='userProperty_property_id')
    dStartDate = models.DateTimeField(blank=True, null= False)
    dEndDate = models.DateTimeField(blank=True, null= False)
    eTypeofTimeshare = models.CharField(max_length=100,choices=TypeofTimeshare.choices)
    eTypeofTransaction = models.CharField(max_length=100,choices=TypeofTransaction.choices)
    iTransactionUserId = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userProperty_transaction_user_id')
    fTransactionAmount = models.FloatField(unique=False,blank=True, null= True)
    fTransactionFee = models.FloatField(unique=False,blank=True, null= True)
    iCurrencyId = models.ForeignKey(CurrencyMaster, on_delete=models.CASCADE,related_name='userProperty_currency_id')
    sJSONObject = models.JSONField()
    iCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userProperty_created_by')
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userProperty_modified_by')
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False)

    class Meta:
        db_table = 'tblUserProperty'


class CountryMaster(models.Model):
    iCountryCode = models.IntegerField(unique=False, blank=True, null= False)
    sCountryName = models.CharField(max_length=100,blank=True, null= False)
    iCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='countryMaster_created_by')
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='countryMaster_modified_by')
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False)
    class Meta:
        db_table = 'tblCountryMaster'


class StateMaster(models.Model):
    sStateName =  models.CharField(max_length=100,blank=True, null= False)
    iCountryid = models.ForeignKey(CountryMaster, on_delete=models.CASCADE,related_name='stateMaster_country_id')
    iCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='stateMaster_created_by')
    dCreatedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    iModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='stateMaster_modified_by')
    dModifiedDate = models.DateTimeField(auto_now_add=True,blank=True, null= False)
    bLogicalDelete = models.BooleanField(unique=False, blank=True, null= False)
    class Meta:
        db_table = 'tblStateMaster'

