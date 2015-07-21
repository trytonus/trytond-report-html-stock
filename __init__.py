# -*- coding: utf-8 -*-
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
