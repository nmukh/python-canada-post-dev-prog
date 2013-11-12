# coding=utf-8

from canada_post.api import CanadaPostAPI
from . import api_details

import unittest

class TestNonContractShipping(unittest.TestCase):
    """
    Tests the Non-Contract Shipping use case  as detailed on Canada 
    Posts's Non-Contract Shipping documentation
    """
    
    def setUp(self):
        self.interface = CanadaPostAPI(
            customer_number=api_details.AUTH.customer_number,
            username=api_details.AUTH.username,
            password=api_details.AUTH.password,
            contract_number=None,
            dev=api_details.AUTH.dev)
    
    #def test_interface_auth(self):
    #    """ Test the CanadaPostAPI interface constructon with Auth object """
    #    interface = CanadaPostAPI(auth = api_details.AUTH)
    #    self.assertEqual(interface.auth.username, api_details.AUTH.username)
    
    def test_interface_kwargs(self):
        """ Test the CanadaPostAPI interface constructor with key word args"""
        self.assertEqual(self.interface.auth.username,
                         api_details.AUTH.username)
    
    def test_create_nc_shipment(self):
        """
        The typical route used for shipping without a Canada Post contract:
        
        * Create Non-Contract Shipment
        
        * Get Artifact
        """
        pass
    
    def test_get_nc_shipment_receipt(self):
        """
        Test the Get Non-Contract Shipment receipt
        """
        pass
    
    def test_get_nc_shipment_details(self):
        """
        Tests Get Non-Contract Shipment Details
        """
    
    def test_get_nc_shipments(self):
        """
        Tests Get Non-Contract Shipments
        """
        self.interface.get_shipments()
        
    
    def test_get_nc_shipment(self):
        """
        Get Non-Contract Shipment
        """
        pass
