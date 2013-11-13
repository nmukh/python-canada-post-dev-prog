"""
Central API module
"""
import logging
import requests

from canada_post import PROD, Auth
from canada_post.service import ServiceBase
from canada_post.service.contract_shipping import (CreateShipment, 
                                                   VoidShipment,
                                                   TransmitShipments,
                                                   GetManifest, GetArtifact,
                                                   GetManifestShipments)
from canada_post.service.rating import (GetRates)
from canada_post.errors import CanadaPostError

logger = logging.getLogger('canada_post.api')


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
        
        ``method`` : The name of a 'requests' function call representing the
                     HTTP method to use. i.e Replaces {method}
        
        ``mobo`` : if true, {mobo} will be populate, otherwise it will be
                   removed
        
        ``url`` : replaces {url}
        
        ``headers`` : a dictionary of headers to be passed to 'requests'`s
                      'post', 'get', or 'delete' functions. It should
                      not include the 'Authorization' header as it is inserted
                      in this function.
        
        ``body`` : TODO. A dictionary-style object used to compile the XML 
                   document to replace {XML}
        
        ``kwargs`` : keyword arguments that will be inserted into 
                     {query string}
        
        
        _[#] Canada Post, "REST Fundamentals of Canada Post Web Services"
        """
        # TODO: Currently returns a 'requests' response, but should return an
        #       instance of 'CanadaPostResponse'
        
        service = ServiceBase(self.auth)
        
        # Compile the url using correct endpoint
        cp_url = "https://{XX}/rs/{mailed_by_customer}/{url}".format(
            XX=service.get_server(),
            mailed_by_customer=self.auth.customer_number,
            url=url)
        
        # compile HTTP headers
        auth = service.userpass() 
        # TODO: assert (or make defaults) that "Content-type" in 
        #       'headers.keys()' if POST and "Accept" in 'headers.keys()' if 
        #       GET
        
        # TODO: compile xml document
        
        # make call
        logger.debug("put the entire HTTP request here")
        assert(method in ["get", "post", "delete"])
        request_method = getattr(requests, method)
        response = request_method(url=cp_url, params=kwargs, data=body, 
                                  headers=headers, auth=auth)
        logger.debug("Canada Post Response Body:\n {0}".format(
            response.content))
        if response.status_code not in [200, 202, 204, 304]:
            raise CanadaPostError(
                response.status_code,
                "Canada Post Error! code : {0}; message : {1}".format(
                    "xxx", "blah blah blah"))
        
        return response
    
    
    def nc_get_shipments(self, from_date, to_date=None):
        """ Shortcut to "Get Non-Contract Shipments - REST"
        
        ``from_date`` and ``to_date`` in "YYYYMMDDHHMM" format
        
        no XML body required
        """
        # TODO: accept actual python date objects instead of date strings
        headers = {
            'Accept': "application/vnd.cpc.ncshipment+xml",
            'Content-Type': 'application/vnd.cpc.ncshipment+xml',
            'Accept-language': 'en-CA',
        }
        
        params = { "from" : from_date }
        if to_date is not None:
            params["to"] = to_date
        
        logger.info("Asking for non-contract shipments from {0} to {1}".format(
                    from_date, to_date))
        return self._call("get", False, "ncshipment", headers, None, **params)
