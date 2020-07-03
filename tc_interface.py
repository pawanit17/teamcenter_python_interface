import sys
import requests
import xml.etree.ElementTree as ET

# Usecase 1: Login to Teamcenter
# ------------------------------
# Python's requests module can be used for leveraging the SOAP calls to Teamcenter.
# Pip install can do the trick of installing the modules if needed. I am using python 2.7
# with the editor as PyCharm Community Version.
url = "https://localhost/tc/services/Core-2006-03-Session?wsdl" # This is the WSDL for login method.
headers = {'Content-Type': 'text/xml', 'SOAPAction': 'login' }
# Understanding SOAP Requests: Different SOA operations have different input structures that are to be populated to make them work.
# The best way to identify this is using SOAPUI. That is a free tool in which you can import the WSDLs of Teamcenter and you can see
# the sample XML request that is prepared for a given SOA operation. You can just copy it and use it in your Python requests.
body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ses="http://teamcenter.com/Schemas/Core/2006-03/Session">
 <soapenv:Header/>
 <soapenv:Body>
 <ses:LoginInput username="dirk" password="dirk" group="" role="" sessionDiscriminator="1i52"/>
 </soapenv:Body>
</soapenv:Envelope>"""

# Ours is HTTPS implementation. So for a quick prototype, I have used the 'verify' as false.
# In practical production grade code, you would have to remove this flag, defaulting it to True.
response = requests.post(url,data=body,headers=headers,verify=False)

# Understanding SOA Responses: The best way for this one is to just print the 'response.content'. The output would be similar
# to what you typically get in the Teamcenter RAC communication monitor view. How you parse to get the relevant information is
# entirely dependent on the SOA that you are using.
if response.status_code == 200:
 print 'Login was successful.'
 print response.content
else:
 print 'Login failed.'
 sys.exit( 'Login operation failed with HTTP Code ' + str( response.status_code ) )

# HTTP is a stateless protocol. It cannot discern between two requests from the same user.
# Two ways out of this - JWT Tokens or Session Identifiers. Teamcenter uses Session Identifiers
# in the form of JSESSIONID. Upon login operation, a JSESSIONID gets returned in the response.
# Example: JSESSIONID - 8heEOiDBF_4UJ1kq9vWLknb5Kf-aTvyqJSflq3xj.localhost
login_session_id = None
for c in response.cookies:
 if c.name == 'JSESSIONID':
 login_session_id = c.value

jsession_token = "JSESSIONID=" + login_session_id
print(jsession_token)


# Usecase 2: Get properties of a Document from Teamcenter
# ---------------------------------
url = "https://localhost/tc/services/Core-2006-03-DataManagement?wsdl" # This is the WSDL for getProperies method.
headers = {'Content-Type': 'text/xml', 'SOAPAction': 'getProperties', 'Cookie' : jsession_token }
body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dat="http://teamcenter.com/Schemas/Core/2006-03/DataManagement" xmlns:base="http://teamcenter.com/Schemas/Soa/2006-03/Base">
 <soapenv:Header/>
 <soapenv:Body>
 <dat:GetPropertiesInput>
 <dat:objects uid="zid5i57744e$yB" type="" classUid="" className="" updateDesc="" objectID="" cParamID="" isHistorical="" isObsolete="" jbt_addition="">
 </dat:objects>
 </dat:GetPropertiesInput>
 </soapenv:Body>
</soapenv:Envelope>"""
response = requests.post(url,data=body,headers=headers,verify=False)
print response.content
root = ET.fromstring( response.content )

response_body = root[0]
response_servicedata = response_body[0]
response_dataobjects = response_servicedata[1]

for objectproperties in response_dataobjects:
 if objectproperties.attrib['name'] == 'object_string':
 print 'The object_string of the puid is ' + objectproperties.attrib['uiValue']

if response.status_code == 200:
 print 'GetProperties was successful.'
 print response.content
else:
 print 'GetProperties failed.'
 sys.exit( 'GetProperties operation failed with HTTP Code ' + str( response.status_code ) )

# Usecase 3: Logout from Teamcenter
# ---------------------------------
url = "https://localhost/tc/services/Core-2006-03-Session?wsdl" # This is the WSDL for logout method.
headers = {'Content-Type': 'text/xml', 'SOAPAction': 'logout', 'Cookie' : jsession_token }
body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ses="http://teamcenter.com/Schemas/Core/2006-03/Session">
 <soapenv:Header/>
 <soapenv:Body>
 <ses:LogoutInput/>
 </soapenv:Body>
</soapenv:Envelope>"""
response = requests.post(url,data=body,headers=headers,verify=False)

if response.status_code == 200:
 print 'Logout was successful.'
 print response.content
else:
 print 'Logout failed.'
 sys.exit( 'Logout operation failed with HTTP Code ' + str( response.status_code ) )

