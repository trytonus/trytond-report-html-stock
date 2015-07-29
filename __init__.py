# -*- coding: utf-8 -*-
from trytond.pool import Pool
from report_html_stock import PickingList, SupplierRestockingList, \
    CustomerReturnRestockingList, ConsolidatedPickingList


def register():
    Pool.register(
        PickingList,
        SupplierRestockingList,
        CustomerReturnRestockingList,
        ConsolidatedPickingList,
        module='report_html_stock', type_='report'
    )
