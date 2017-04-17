# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER
from trytond.transaction import Transaction
from trytond.pyson import Eval


class BaseTestCase(unittest.TestCase):
    '''
    Base Test Case for report_html_stock module.
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module('report_html_stock')

        self.Currency = POOL.get('currency.currency')
        self.Company = POOL.get('company.company')
        self.Party = POOL.get('party.party')
        self.User = POOL.get('res.user')
        self.ProductTemplate = POOL.get('product.template')
        self.Uom = POOL.get('product.uom')
        self.ProductCategory = POOL.get('product.category')
        self.Product = POOL.get('product.product')
        self.Country = POOL.get('country.country')
        self.Subdivision = POOL.get('country.subdivision')
        self.Employee = POOL.get('company.employee')
        self.Location = POOL.get('stock.location')
        self.ShipmentOut = POOL.get('stock.shipment.out')
        self.StockLocation = POOL.get('stock.location')
        self.Address = POOL.get('party.address')
        self.Move = POOL.get('stock.move')
        self.Product = POOL.get('product.product')
        self.ShipmentIn = POOL.get('stock.shipment.in')
        self.ShipmentOutReturn = POOL.get('stock.shipment.out.return')
        self.Sale = POOL.get('sale.sale')
        self.SaleLine = POOL.get('sale.line')

    def _create_coa_minimal(self, company):
        """Create a minimal chart of accounts
        """
        AccountTemplate = POOL.get('account.account.template')
        Account = POOL.get('account.account')

        account_create_chart = POOL.get(
            'account.create_chart', type="wizard")

        account_template, = AccountTemplate.search([
            ('parent', '=', None),
            ('name', '=', 'Minimal Account Chart')
        ])

        session_id, _, _ = account_create_chart.create()
        create_chart = account_create_chart(session_id)
        create_chart.account.account_template = account_template
        create_chart.account.company = company
        create_chart.transition_create_account()

        receivable, = Account.search([
            ('kind', '=', 'receivable'),
            ('company', '=', company),
        ])
        payable, = Account.search([
            ('kind', '=', 'payable'),
            ('company', '=', company),
        ])
        create_chart.properties.company = company
        create_chart.properties.account_receivable = receivable
        create_chart.properties.account_payable = payable
        create_chart.transition_create_properties()

    def _get_account_by_kind(self, kind, company=None, silent=True):
        """Returns an account with given spec
        :param kind: receivable/payable/expense/revenue
        :param silent: dont raise error if account is not found
        """
        Account = POOL.get('account.account')
        Company = POOL.get('company.company')

        if company is None:
            company, = Company.search([], limit=1)

        accounts = Account.search([
            ('kind', '=', kind),
            ('company', '=', company)
        ], limit=1)
        if not accounts and not silent:
            raise Exception("Account not found")

        if not accounts:
            return None
        account, = accounts

        return account

    def _create_payment_term(self):
        """Create a simple payment term with all advance
        """
        PaymentTerm = POOL.get('account.invoice.payment_term')

        return PaymentTerm.create([{
            'name': 'Direct',
            'lines': [('create', [{'type': 'remainder'}])]
        }])

    def setup_defaults(self):
        """Creates default data for testing
        """

        self.currency, = self.Currency.create([{
            'name': 'US Dollar',
            'code': 'USD',
            'symbol': '$',
        }])

        with Transaction().set_context(company=None):
            self.company_party, = self.Party.create([{
                'name': 'openlabs',
            }])

        self.company, = self.Company.create([{
            'party': self.company_party,
            'currency': self.currency,
        }])
        self.User.write([self.User(USER)], {
            'company': self.company,
            'main_company': self.company,
        })

        Transaction().context.update(
            self.User.get_preferences(context_only=True)
        )

        self.country, = self.Country.create([{
            'name': 'United States of America',
            'code': 'US',
        }])
        self.subdivision, = self.Subdivision.create([{
            'country': self.country.id,
            'name': 'California',
            'code': 'CA',
            'type': 'state',
        }])

        self._create_coa_minimal(self.company)

        self._create_payment_term()

        self.party, = self.Party.create([{
            'name': 'Bruce Wayne',
            'addresses': [('create', [{
                'name': 'Bruce Wayne',
                'party': Eval('id'),
                'city': 'Gotham',
                'country': self.country.id,
                'subdivision': self.subdivision.id,
            }])],
            'contact_mechanisms': [('create', [
                {'type': 'mobile', 'value': '8888888888'},
            ])],
        }])
        self.Party.write([self.company.party], {
            'addresses': [('create', [{
                'name': 'Lie Nielsen',
                'city': 'Los Angeles',
                'country': self.country.id,
                'subdivision': self.subdivision.id,
            }])],
        })
        self.product_category, = self.ProductCategory.create([{
            'name': 'Automobile',
        }])
        self.uom, = self.Uom.search([('name', '=', 'Unit')])

        self.product_template, = self.ProductTemplate.create([{
            'name': 'Bat Mobile',
            'type': 'goods',
            'categories': [('add', [self.product_category.id])],
            'list_price': Decimal('20000'),
            'cost_price': Decimal('15000'),
            'default_uom': self.uom.id,
        }])
        self.product, = self.Product.create([{
            'template': self.product_template.id,
            'code': '123',
        }])
