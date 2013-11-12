"""
Central API module
"""
from canada_post import PROD, Auth
from canada_post.service.contract_shipping import (CreateShipment, VoidShipment,
                                                   TransmitShipments,
                                                   GetManifest, GetArtifact,
                                                   GetManifestShipments,
                                                   GetShipments)
from canada_post.service.rating import (GetRates)

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
        
    def get_shipments(self, date_str=None, limit=None, group_id=None, 
             manifest=None):
        """ Shortcut to the GetShipments method
        """
        method = GetShipments(self.auth)
        return method(date_str, limit, group_id, manifest)
