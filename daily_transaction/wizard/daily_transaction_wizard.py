from odoo import models, fields, api

class DailyTransactionWizard(models.TransientModel):
    _name = 'daily.transaction.wizard'
    _description = 'Daily Transaction Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def print_report(self):
        journal_data = []
        journal_items = self.env['account.move.line'].search([
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date)
        ])

        journal_dict = {}
        for item in journal_items:
            journal_name = item.move_id.journal_id.name
            if journal_name not in journal_dict:
                journal_dict[journal_name] = []
            journal_dict[journal_name].append({
                'date': item.date.strftime('%Y-%m-%d'),
                'move_name': item.move_id.name,
                'account_name': item.account_id.name,
                'debit': item.debit,
                'credit': item.credit
            })

        for journal, transactions in journal_dict.items():
            journal_data.append({'journal_name': journal, 'transactions': transactions})

        data = {
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'journal_data': journal_data
        }

        return self.env.ref('daily_transaction.daily_transaction_report_action').report_action(self, data=data)
