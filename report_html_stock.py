# -*- coding: utf-8 -*-
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

from openlabs_report_webkit import ReportWebkit

__all__ = [
    'PickingList', 'SupplierRestockingList', 'CustomerReturnRestockingList'
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

    @classmethod
    def parse(cls, report, records, data, localcontext):

        sorted_moves = cls.get_sorted_moves(records)

        localcontext['moves'] = sorted_moves

        return super(PickingList, cls).parse(
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
