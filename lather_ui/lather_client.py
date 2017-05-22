# Written with suds-py3 and python 3.6.1
from suds.client import Client
import suds

import datetime

try:
    from urllib.parse import urlparse

except:
    from urlparse import urlparse


"""
#LOGGING
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
"""

class ConfigurationPersistence():
    """
    This is a class for writing and reading configuration files for persistent settings.
    All settings will be encrypted eventually using my custom encryption module (not currently in this project,
    as it's Windows Only so far)

    This will also have a few boolean values for "does exist" to trigger certain logic in the UI
    """
    def __init__(self):
        pass

class SudsClientExtension(Client):
    """
    Adding a few things and changing a few things for the __str__ method to make the UI easier to build
    """
    def to_dict(self):
        s = ['\n']
        for sd in self.sd:
            text = self.get_sd_description(sd)
            s.append('\n\n%s' %text)
        return str(text)

    @staticmethod
    def get_sd_description(sd):
        # Yanking out of the ServiceDefinition class within Suds, will re-work this to produce the dictionary
        # object I need for auto-discovery in the UI
        """
        Get a textual description of the service for which this object
        represents.
        @return: A textual description.
        @rtype: str
        """
        result = {}
        service_name = sd.service.name + " " + sd.wsdl.tns[1]
        result[service_name] = {}
        result[service_name]['prefixes'] = []
        for p in sd.prefixes:
            result[service_name]['prefixes'].append('%s = "%s"' % p)
        result[service_name]['ports'] = {}
        for p in sd.ports:
            port = p[0].name
            result[service_name]['ports'][port] = {}
            result[service_name]['ports'][port]['methods']= {}
            for m in p[1]:
                result[service_name]['ports'][port]['methods'][m[0]] = []
                for p in m[1]:
                    result[service_name]['ports'][port]['methods'][m[0]].append(sd.xlate(p[1]) + " " + p[0])
            result[service_name]['ports'][port]['types'] = []
            for t in sd.types:
                result[service_name]['ports'][port]['types'].apped(sd.xlate(t[0]))
        return result


class SudsClientWrapper():
    def __init__(self, wsdl_url, custom_headers=None):
        self._client = SudsClientExtension(wsdl_url, headers=custom_headers)
        self._interface = str(self._client)
        self.interfaceDetails = self.buildMethodDetails(self.enumerateMethods())
        self.auto_discovered_services = self._client.to_dict()
        print(self.auto_discovered_services)
    def enumerateMethods(self):
        functions = [m for m in self._client.wsdl.services[0].ports[0].methods]
        return functions

    def getParamType(self, param):
        param_name = param[1]
        param_type = param[0]
        if param_type.split(':')[0] is not "xs":
            print(param_type)

    def buildMethodDetails(self, functions):
        # TODO: Reimplement this in a much smarter way...
        """
        This is run at client instantiation, this will parse out the details of the suds client
        into dictionaries that are used to build forms for arbitrary soap methods.
        """
        lines = self._interface.split('\n')
        methodDetails = {}
        for f in functions:
            methodDetails[f] = {}
            for line in lines:
                if (f+'(') in line:
                    line = line.rstrip(" ")
                    line = line.lstrip(" ")
                    methodDetails[f]['signature'] = line
                    methodDetails[f]['params'] = []
                    discard, params = methodDetails[f]['signature'].split('(')
                    methodDetails[f]['params'] = []
                    for param in params.split(','):
                        if ")" not in param:
                            param = param.lstrip(" ")
                            param = param.rstrip(" ")
                            param_type, param_name = param.split(' ')
                            methodDetails[f]['params'].append((param_type, param_name))
        print(methodDetails)
        return methodDetails

    def parseInterfaceDetails(self):
        """ Parses the suds client string to generate forms, buttons, and other useful stuff. """
        interfacedetails = {}


    def getMethodSignature(self, name):
        method_signature = self.interfaceDetails[name]
        print(method_signature)
        return method_signature

    def getXMLRequest(self):
        return self._client.last_sent()

    def getXMLResponse(self):
        return self._client.last_received()

    def convertRequestParams(self, call_params):
        return_params = {}
        for key in call_params.keys():
            type, name = key.split(' ')
            if type == "xs:date":
                year, month, day = call_params[key].split('-')
                return_params[name] = datetime.date(int(year), int(month), int(day))
            elif type == "xs:string":
                return_params[name] = str(call_params[key])
            elif type == "xs:decimal":
                return_params[name] = float(call_params[key])
            else:
                pass
        return return_params

    def sendCall(self, method_name, call_params):
        method = getattr(self._client.service, method_name)
        kwargs = self.convertRequestParams(call_params)
        method(**kwargs)

    def showXMLInAndOut(self):
        # TODO: Remove this...
        print("  --  Requested XML --  ")
        print(self.getXMLRequest())
        print("  --  Response XML  --  ")
        print(self.getXMLResponse())

if __name__ == '__main__':
    # This service has multiple ports... further debugging and adjustment needed in building method_details
    url = 'http://www.webservicex.com/globalweather.asmx?WSDL'
    soap_client = SudsClientWrapper(url)
    method_name = 'some method name'
    method = getattr(soap_client._client.service, method_name)
    method_signature = soap_client.interfaceDetails[method_name]['signature']
    method_params = soap_client.interfaceDetails[method_name]['params']

    call_params = {}
    for param in method_params:
        param_value = input("%s :  " %(param[1]))
        if param[0] == "xs:date":
            split_date = param_value.split('-')
            print(split_date)
            param_value = datetime.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        if param_value is not "":
            call_params[param[1]] = (param_value)

    method(**call_params)
    soap_client.showXMLInAndOut()

"""
    Available URLs for Testing 

    http://www.webservicex.com/stockquote.asmx?WSDL

    http://www.predic8.com:8080/shop/ShopService?wsdl

    http://www2.soriana.com/integracion/recibecfd/wseDocRecibo.asmx?wsdl

    
"""