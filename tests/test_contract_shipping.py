# coding=utf-8

import unittest

from canada_post.service import contract_shipping, Service
from canada_post.util import parcel, address
from . import api_details

class TestContractShipping(unittest.TestCase):
    """
    Tests the functions specific to contract shipping as detailed on Canada 
    Posts's Contract Shipping documentation
    """
    
    def setUp(self):
        self.parcel = parcel.Parcel(
            weight=1, length=20, width=20, height=10
        )
        self.origin = address.Origin(
            postal_code="H3Z2Y7",
            name="John Jones",
            company="Company Co.",
            phone="5145555555",
            address="10-123 1/2 Main St. SE",
            city="Montreal",
            province="Quebec"
        )
        self.destination = address.Destination(
            postal_code="V8X3X4",
            name="Jane Jones",
            phone="6145555555",
            address="1425 James St.",
            city="Victoria",
            province="British Columbia",
            country_code="CA"
        )
        self.service = Service(data={"name": "Expedited Parcel", 
                                     "code": "DOM.EP"})
    
    
    def test_create_shipment(self):
        cp_req = contract_shipping.CreateShipment(api_details.AUTH)
        cp_req(self.parcel, self.origin, self.destination, self.service,
               "fake_group_id")
    
    def test_get_shipment(self):
        pass
    
    def test_get_artifact(self):
        pass
    
    def test_get_shipment_price(self):
        pass
    
    def test_get_shipment_receipt(self):
        pass
    
    def test_get_shipment_details(self):
        pass
    
    def test_get_groups(self):
        pass
    
    def test_get_shipments(self):
        pass
    
    def test_void_shipment(self):
        pass

