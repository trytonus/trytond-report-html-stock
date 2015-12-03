# -*- coding: utf-8 -*-
from trytond.pool import Pool
from stock import ShipmentOut, Move
from report_html_stock import PickingList, SupplierRestockingList, \
    CustomerReturnRestockingList, ConsolidatedPickingList, DeliveryNote, \
    ProductLedger, ProductLedgerStartView, ProductLedgerReport, ItemsWaitingShipmentReport, \
    ItemsWaitingShipmentStart, ItemsWaitingShipmentReportWizard


def register():
    Pool.register(
        ShipmentOut,
        Move,
        ProductLedgerStartView,
        ItemsWaitingShipmentStart,
        module='report_html_stock', type_='model'
    )
    Pool.register(
        ProductLedger,
        ItemsWaitingShipmentReportWizard,
        module='report_html_stock', type_='wizard'
    )
    Pool.register(
        PickingList,
        SupplierRestockingList,
        CustomerReturnRestockingList,
        ConsolidatedPickingList,
        DeliveryNote,
        ProductLedgerReport,
        ItemsWaitingShipmentReport,
        module='report_html_stock', type_='report'
    )
