# -*- coding: utf-8 -*-
from trytond.pool import Pool
from stock import ShipmentOut, Move
from report_html_stock import PickingList, SupplierRestockingList, \
    CustomerReturnRestockingList, ConsolidatedPickingList


def register():
    Pool.register(
        ShipmentOut,
        Move,
        module='report_html_stock', type_='model'
    )
    Pool.register(
        PickingList,
        SupplierRestockingList,
        CustomerReturnRestockingList,
        ConsolidatedPickingList,
        module='report_html_stock', type_='report'
    )
