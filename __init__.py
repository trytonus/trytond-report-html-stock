# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from report_html_stock import PickingList, SupplierRestockingList
from report_html_stock import CustomerReturnRestockingList


def register():
    Pool.register(
        PickingList,
        SupplierRestockingList,
        CustomerReturnRestockingList,
        module='report_html_stock', type_='report'
    )
