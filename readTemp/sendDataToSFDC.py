#import cgi
#import requests
#import json
from simple_salesforce import Salesforce

#security_token='IOeniVBP22UQK7r0vRKitYUVF'

sf=Salesforce(username='sshere@tempsensor.org',password='Sensor20',security_token='IOeniVBP22UQK7r0vRKitYUVF');
sf.Temperature__c.create({'Name':'temp1','Temperature__c':'22.3'})

