# -*- coding: utf-8 -*-
from trytond.pool import Pool
from stock import ShipmentOut, Move
from report_html_stock import PickingList, SupplierRestockingList, \
    CustomerReturnRestockingList, ConsolidatedPickingList, DeliveryNote


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
        DeliveryNote,
        module='report_html_stock', type_='report'
    )
