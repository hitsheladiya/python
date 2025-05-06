from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class DailyTransactionReport(models.AbstractModel):
    _name = 'report.daily_transaction.daily_transaction_report_template'
    _description = 'Daily Transaction Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        journal_data = []
        journals = self.env['account.journal'].search([])

        for journal in journals:
            transactions = self.env['account.move.line'].search([
                ('journal_id', '=', journal.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date)
            ])
            
            if transactions:
                journal_data.append({
                    'journal_name': journal.name,
                    'transactions': [{
                        'date': t.date.strftime('%Y-%m-%d'),
                        'move_name': t.move_id.name,
                        'account_name': t.account_id.name,
                        'debit': t.debit,
                        'credit': t.credit
                    } for t in transactions]
                })

        _logger.info("🛠️ FINAL DATA SENT TO REPORT: %s", journal_data)

        return {
            'data': {
                'start_date': start_date,
                'end_date': end_date,
                'journal_data': journal_data
            }
        }