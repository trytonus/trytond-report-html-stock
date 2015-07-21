# -*- coding: utf-8 -*-
import sys
import os
import unittest

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction
from trytond.pool import Pool

from test_base import BaseTestCase

DIR = os.path.abspath(os.path.normpath(os.path.join(
    __file__, '..', '..', '..', '..', '..', 'trytond'
)))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))


class TestShipment(BaseTestCase):
    """
    Test Picking List
    """

    @unittest.skipIf(sys.platform == 'darwin', 'wkhtmltopdf repo on OSX')
    def test_0110_test_picking_list_report(self):
        """
        Test picking list report
        """
        Report = POOL.get('report.picking_list', type="report")
        Date = POOL.get('ir.date')
        ActionReport = POOL.get('ir.action.report')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()

            with Transaction().set_context({'company': self.company.id}):
                shipment, = self.ShipmentOut.create([{
                    'planned_date': Date.today(),
                    'effective_date': Date.today(),
                    'customer': self.party.id,
                    'warehouse': self.StockLocation.search([
                        ('type', '=', 'warehouse')
                    ])[0],
                    'delivery_address': self.party.addresses[0],
                }])
                move1, = self.Move.create([{
                    'shipment': ('stock.shipment.out', shipment.id),
                    'product': self.product.id,
                    'uom': self.uom.id,
                    'quantity': 6,
                    'from_location': shipment.warehouse.storage_location.id,
                    'to_location': shipment.warehouse.output_location.id,
                }])

                # Change the report extension to PDF
                action_report, = ActionReport.search([
                    ('name', '=', 'Picking List'),
                    ('report_name', '=', 'report.picking_list')
                ])
                action_report.extension = 'pdf'
                action_report.save()

                # Set Pool.test as False as we need the report to be generated
                # as PDF
                # This is specifically to cover the PDF coversion code
                Pool.test = False

                # Generate Picking List Report
                val = Report.execute([shipment.id], {})

                # Revert Pool.test back to True for other tests to run normally
                Pool.test = True

                self.assertTrue(val)
                # Assert report type
                self.assertEqual(val[0], 'pdf')
                # Assert report name
                self.assertEqual(val[3], 'Picking List')

    @unittest.skipIf(sys.platform == 'darwin', 'wkhtmltopdf repo on OSX')
    def test_0120_test_supplier_restocking_list_report(self):
        """
        Test Supplier Restocking list report
        """
        Report = POOL.get('report.supplier_restocking_list', type="report")
        Date = POOL.get('ir.date')
        ActionReport = POOL.get('ir.action.report')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()

            with Transaction().set_context({'company': self.company.id}):
                shipment, = self.ShipmentIn.create([{
                    'planned_date': Date.today(),
                    'effective_date': Date.today(),
                    'supplier': self.party.id,
                    'warehouse': self.StockLocation.search([
                        ('type', '=', 'warehouse')
                    ])[0],
                }])
                move1, = self.Move.create([{
                    'shipment': ('stock.shipment.in', shipment.id),
                    'product': self.product.id,
                    'uom': self.uom.id,
                    'quantity': 6,
                    'from_location': shipment.warehouse.input_location.id,
                    'to_location': shipment.warehouse.storage_location.id,
                }])

                # Change the report extension to PDF
                action_report, = ActionReport.search([
                    ('name', '=', 'Supplier Restocking List'),
                    ('report_name', '=', 'report.supplier_restocking_list')
                ])
                action_report.extension = 'pdf'
                action_report.save()

                # Set Pool.test as False as we need the report to be generated
                # as PDF
                # This is specifically to cover the PDF coversion code
                Pool.test = False

                # Generate Supplier Restocking List Report
                val = Report.execute([shipment.id], {})

                # Revert Pool.test back to True for other tests to run normally
                Pool.test = True

                self.assertTrue(val)
                # Assert report type
                self.assertEqual(val[0], 'pdf')
                # Assert report name
                self.assertEqual(val[3], 'Supplier Restocking List')

    @unittest.skipIf(sys.platform == 'darwin', 'wkhtmltopdf repo on OSX')
    def test_0130_test_Customer_restocking_list_report(self):
        """
        Test Supplier Restocking list report
        """
        Report = POOL.get('report.customer_return_restocking_list',
                          type="report")
        Date = POOL.get('ir.date')
        ActionReport = POOL.get('ir.action.report')

        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.setup_defaults()

            with Transaction().set_context({'company': self.company.id}):
                shipment, = self.ShipmentOutReturn.create([{
                    'planned_date': Date.today(),
                    'effective_date': Date.today(),
                    'customer': self.party.id,
                    'warehouse': self.StockLocation.search([
                        ('type', '=', 'warehouse')
                    ])[0],
                    'delivery_address': self.party.addresses[0],
                }])
                move1, = self.Move.create([{
                    'shipment': ('stock.shipment.out.return', shipment.id),
                    'product': self.product.id,
                    'uom': self.uom.id,
                    'quantity': 6,
                    'from_location': shipment.warehouse.input_location.id,
                    'to_location': shipment.warehouse.storage_location.id,
                }])

                # Change the report extension to PDF
                action_report, = ActionReport.search([
                    ('name', '=', 'Customer Restocking List'),
                    ('report_name', '=',
                     'report.customer_return_restocking_list')
                ])
                action_report.extension = 'pdf'
                action_report.save()

                # Set Pool.test as False as we need the report to be generated
                # as PDF
                # This is specifically to cover the PDF coversion code
                Pool.test = False

                # Generate Customer Restocking List Report
                val = Report.execute([shipment.id], {})

                # Revert Pool.test back to True for other tests to run normally
                Pool.test = True

                self.assertTrue(val)
                # Assert report type
                self.assertEqual(val[0], 'pdf')
                # Assert report name
                self.assertEqual(val[3], 'Customer Restocking List')


def suite():
    "Define suite"
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestShipment)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
