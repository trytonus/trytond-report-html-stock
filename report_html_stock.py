# -*- coding: utf-8 -*-
from itertools import groupby, imap, chain

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

from openlabs_report_webkit import ReportWebkit

__all__ = [
    'PickingList', 'SupplierRestockingList', 'CustomerReturnRestockingList',
    'ConsolidatedPickingList'
]
__metaclass__ = PoolMeta


class ReportMixin(ReportWebkit):
    """
    Mixin Class to inherit from, for all HTML reports.
    """

    @classmethod
    def wkhtml_to_pdf(cls, data, options=None):
        """
        Call wkhtmltopdf to convert the html to pdf
        """
        Company = Pool().get('company.company')

        company = ''
        if Transaction().context.get('company'):
            company = Company(Transaction().context.get('company')).party.name
        options = {
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'margin-right': '0.50in',
            'margin-top': '0.50in',
            'footer-font-size': '8',
            'footer-left': company,
            'footer-line': '',
            'footer-right': '[page]/[toPage]',
            'footer-spacing': '5',
        }
        return super(ReportMixin, cls).wkhtml_to_pdf(
            data, options=options
        )

    @classmethod
    def get_sorted_moves(cls, records):
        """
        Sorting the moves for each shipment
        """
        sorted_moves = {}
        for shipment in records:
            sorted_moves[shipment.id] = sorted(
                shipment.inventory_moves,
                key=lambda m: (m.from_location, m.to_location)
            )
        return sorted_moves


class PickingList(ReportMixin):
    """
    Picking List Report
    """
    __name__ = 'report.picking_list'

    @staticmethod
    def sort_inventory_moves(shipment, sort_key=None):
        """
        A sorter that can be overwritten by downstream modules
        """
        return sorted(shipment.inventory_moves, key=sort_key)

    @classmethod
    def parse(cls, report, records, data, localcontext):
        localcontext['sort_inventory_moves'] = cls.sort_inventory_moves
        localcontext['sort_key'] = lambda move: (
            move.from_location.rec_name, move.product.name
        )
        return super(PickingList, cls).parse(
            report, records, data, localcontext
        )


class ConsolidatedPickingList(ReportMixin):
    """
    Consolidated Picking List.
    """
    __name__ = 'report.consolidated_picking_list'

    @classmethod
    def group_key(cls, move):
        """
        Key function for grouping and sorting of
        moves
        """
        return (move.from_location, move.product)

    @classmethod
    def get_product_repr_from(cls, key):
        """
        Returns the product representation from the key
        """
        return key[1].rec_name

    @classmethod
    def get_location_repr_from(cls, key):
        """
        Returns the location representation from the key
        """
        return key[0].rec_name

    @classmethod
    def parse(cls, report, records, data, localcontext):
        """
        The default implementation groups by product
        and sorts by from_location.
        """
        localcontext['grouped_moves'] = []
        for key, grouper in groupby(
                # Sort all the moves from all shipments
                # and then group it
                list(sorted(
                    # Chain all inventory moves from all shipments
                    chain(*imap(lambda s: s.inventory_moves, records)),
                    key=cls.group_key
                )), cls.group_key):
            moves = list(grouper)
            # TODO: Sum totals everything, the UOM to base UOM conversion
            # is not done
            localcontext['grouped_moves'].append(
                (key, moves, sum(map(lambda m: m.quantity, moves)))
            )

        localcontext['get_product_repr_from'] = cls.get_product_repr_from
        localcontext['get_location_repr_from'] = cls.get_location_repr_from
        return super(ConsolidatedPickingList, cls).parse(
            report, records, data, localcontext
        )


class SupplierRestockingList(ReportMixin):
    'Supplier Restocking List'
    __name__ = 'report.supplier_restocking_list'

    @classmethod
    def parse(cls, report, records, data, localcontext):

        sorted_moves = cls.get_sorted_moves(records)

        localcontext['moves'] = sorted_moves

        return super(SupplierRestockingList, cls).parse(
            report, records, data, localcontext
        )


class CustomerReturnRestockingList(ReportMixin):
    'Customer Return Restocking List'
    __name__ = 'report.customer_return_restocking_list'

    @classmethod
    def parse(cls, report, records, data, localcontext):

        sorted_moves = cls.get_sorted_moves(records)

        localcontext['moves'] = sorted_moves

        return super(CustomerReturnRestockingList, cls).parse(
            report, records, data, localcontext
        )


class DeliveryNote(ReportMixin):
    "Delivery Note"
    __name__ = 'report.delivery_note'
