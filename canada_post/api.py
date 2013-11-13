"""
Central API module
"""
import requests

from canada_post import PROD, Auth
from canada_post.service import ServiceBase
from canada_post.service.contract_shipping import (CreateShipment, VoidShipment,
                                                   TransmitShipments,
                                                   GetManifest, GetArtifact,
                                                   GetManifestShipments)
from canada_post.service.rating import (GetRates)
from canada_post.errors import CanadaPostError

class CanadaPostAPI(object):
    """ The principle interface for the user """
    
    def __init__(self, customer_number, username, password, contract_number="",
                 dev=PROD):
        self.auth = Auth(customer_number, username, password, contract_number,
                         dev)
        self.get_rates = GetRates(self.auth)
        self.create_shipment = CreateShipment(self.auth)
        self.void_shipment = VoidShipment(self.auth)
        self.transmit_shipments = TransmitShipments(self.auth)
        self.get_manifest = GetManifest(self.auth)
        self.get_artifact = GetArtifact(self.auth)
        self.get_manifest_shipments = GetManifestShipments(self.auth)
        
    def _call(self, method, mobo, url, headers, body, **kwargs):
        """
        A generic calling function.
        
        Canada Post web service request: [#]_
            
            {method}
            + https://{XX}/rs/{mailed by customer}/{mobo}/{url}
            + ?{query string}
            + {HTTP header variables}
            + {XML}
        
        ``method`` : HTTP method to use. Replaces {method}
        
        ``mobo`` : if true, {mobo} will be populate, otherwise it will be
                   removed
        
        ``url`` : replaces {url}
        
        ``headers`` : a dictionary of headers to be passed to 'requests'`s
                      'post', 'get', or 'delete' functions. It should
                      not include the 'Authorization' header as it is inserted
                      in this function.
        
        ``body`` : TODO ... does nothing at this point, but will be used to
                   compile the {XML} body ot the request
        
        ``kwargs`` : keyword arguments that will be inserted into 
                     {query string}
        
        
        _[#] Canada Post, "REST Fundamentals of Canada Post Web Services"
        """
        
        
        # Compile the url using correct endpoint
        service = ServiceBase(self.auth)
        cp_url = "https://{XX}/rs/{mailed_by_customer}/{url}".format(
            XX=service.get_server(),
            mailed_by_customer=self.auth.username,
            url=url)
        
        # compile HTTP headers
        auth = service.userpass() 
        # TODO: assert (or make defaults) that "Content-type" in 
        #       'headers.keys()' if POST and "Accept" in 'headers.keys()' if 
        #       GET
        
        # compile xml document
        # TODO: Maybe take a dictionary of xml element tree as argument to this
        #       fucntion
        
        # make call
        try:
            return requests.post(url=cp_url, params=kwargs, data=body, 
                                 headers=headers, auth=auth)
        except CanadaPostError as e:
            raise e
    
    
    def nc_get_shipments(self, from_date, to_date=None):
        """ Shortcut to the "Get Non-Contract Shipments" method 
        
        ``from_date`` and ``to_date`` in "YYYYMMDDHHMM" format
        
        no body required
        """
        #TODO: Does this have the same exact result as regular get shipments
        #      with the noManifest=true param?
        headers = {
            'Accept': "application/vnd.cpc.ncshipment+xml",
            'Content-Type': 'application/vnd.cpc.ncshipment+xml',
            'Accept-language': 'en-CA',
        }
        
        params = { "from" : from_date }
        if to_date is not None:
            params["to"] = to_date
        
        return self._call("GET", False, "ncshipment", headers, "", **params)
