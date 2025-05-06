# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
import json
from ast import literal_eval
from datetime import datetime
from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.osv.expression import OR, AND
from odoo.tools import date_utils

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if request.env.user.has_group('do_video_conference.group_website_meeting_admin'):
            values['meeting_count'] = request.env['calendar.event'].search_count([])
        return values

    def _meeting_get_page_view_values(self, meeting, access_token, **kwargs):
        mode = 'readonly'
        if kwargs.get('mode'):
            mode = kwargs.get('mode')
        values = {
            'page_name': 'meeting',
            'meeting': meeting,
            'user': request.env.user,
            'mode': mode,
        }
        return self._get_page_view_values(meeting, access_token, values, 'my_meetings_history', False, **kwargs)

    @http.route(['/my/meetings', '/my/meetings/page/<int:page>'], type='http', auth="user", methods=['GET'], website=True)
    def portal_my_meetings(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                           search_in='content', groupby='meeting', **kwargs):
        values = self._prepare_portal_layout_values()
        CalendarEvent = request.env['calendar.event']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_inputs = {
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [("start", "=", today)]},
            'week': {'label': _('This week'), 'domain': [('start', '>=', date_utils.start_of(today, "week")),
                                                         ('start', '<=', date_utils.end_of(today, 'week'))]},
            'month': {'label': _('This month'), 'domain': [('start', '>=', date_utils.start_of(today, 'month')),
                                                           ('start', '<=', date_utils.end_of(today, 'month'))]},
            'year': {'label': _('This year'), 'domain': [('start', '>=', date_utils.start_of(today, 'year')),
                                                         ('start', '<=', date_utils.end_of(today, 'year'))]},
            'quarter': {'label': _('This Quarter'),
                        'domain': [('start', '>=', quarter_start), ('start', '<=', quarter_end)]},
            'last_week': {'label': _('Last week'), 'domain': [('start', '>=', date_utils.start_of(last_week, "week")),
                                                              ('start', '<=', date_utils.end_of(last_week, 'week'))]},
            'last_month': {'label': _('Last month'),
                           'domain': [('start', '>=', date_utils.start_of(last_month, 'month')),
                                      ('start', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': _('Last year'), 'domain': [('start', '>=', date_utils.start_of(last_year, 'year')),
                                                              ('start', '<=', date_utils.end_of(last_year, 'year'))]},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])
        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('calendar.event', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_ids', 'ilike', search)]])
            domain += search_domain

        meeting_count = CalendarEvent.search_count(domain)
        # pagers
        pager = portal_pager(
            url="/my/meetings",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in},
            total=meeting_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        meetings = CalendarEvent.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_meetings_history'] = meetings.ids[:100]
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'meetings': meetings,
            'page_name': 'meeting',
            # 'archive_groups': archive_groups,
            'default_url': '/my/meetings',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'search_in': search_in,
            'sortby': sortby,
            'filterby': filterby,
        })
        return request.render("do_video_conference.portal_my_meetings", values)

    def datetime(self, field_input):
        # lang = request.env['ir.qweb.field'].user_lang()
        # strftime_format = (u"%s %s" % (lang.date_format, lang.time_format))
        # user_tz = pytz.timezone(request.context.get('tz') or request.env.user.tz or 'UTC')
        # dt = user_tz.localize(datetime.strptime(field_input, strftime_format)).astimezone(pytz.utc)
        # return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        user_tz = pytz.timezone(request.env.user.tz or 'UTC')
        dt = user_tz.localize(datetime.strptime(field_input, "%Y-%m-%dT%H:%M")).astimezone(pytz.utc)
        return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _tag_to_write_vals(self, tags=''):
        post_tags = []
        existing_keep = []
        for tag in (tag for tag in tags.split(',') if tag):
            existing_keep.append(int(tag))
        post_tags.insert(0, [6, 0, existing_keep])
        return post_tags

    def meeting_values(self, **kwargs):
        if kwargs.get('participant_history_ids_length'):
            del kwargs['participant_history_ids_length']
        if kwargs.get('attachment_history_ids_length'):
            del kwargs['attachment_history_ids_length']
        if kwargs.get('notes_ids_length'):
            del kwargs['notes_ids_length']
        if 'edit_save' in kwargs:
            kwargs.pop('edit_save')
        if 'mode' in kwargs:
            kwargs.pop('mode')
        if kwargs.get('start'):
            kwargs.update({'start': self.datetime(kwargs.get('start'))})
        if kwargs.get('stop'):
            kwargs.update({'stop': self.datetime(kwargs.get('stop'))})
        tag_write_fields_list = ['partner_ids', 'document_list_preview_user_ids',
                                 'document_delete_ids']
        for tag_list in tag_write_fields_list:
            if kwargs.get(tag_list):
                kwargs.update({tag_list: self._tag_to_write_vals(kwargs.get(tag_list))})
            elif not kwargs.get(tag_list):
                kwargs.update({tag_list: [[6, 0, []]]})
        boolean_fields_check_list = ['video_conference', 'chat_jitsi', 'anonymous_participant',
                                     'bbb_allow_to_record_meeting', 'bbb_allow_start_stop_recording',
                                     'bbb_auto_start_recording', 'bbb_mute_on_start', 'document_list_preview',
                                     'document_delete',
                                     'is_otp_enable', 'otp_type_email']
        for bolean_list in boolean_fields_check_list:
            if kwargs.get(bolean_list):
                kwargs.update({bolean_list: True})
            else:
                kwargs.update({bolean_list: False})
        return kwargs

    @http.route(['/my/meeting/<int:meeting_id>'], type='http', auth="user", methods=['GET', 'POST'], website=True,
                cors='*')
    def portal_my_meeting(self, meeting_id, access_token=None, **kwargs):
        try:
            calendar_sudo = self._document_check_access('calendar.event', meeting_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._meeting_get_page_view_values(calendar_sudo, access_token, **kwargs)
        if kwargs.get('id') and calendar_sudo:
            meeting_values = self.meeting_values(**kwargs)
            calendar_sudo.write(meeting_values)
        if kwargs.get('mode') and kwargs.get('mode') == 'closed' and calendar_sudo:
            calendar_sudo.action_close_meeting()
            return request.redirect('/my/meetings')
        if kwargs.get('mode') and kwargs.get('mode') == 'reopen' and calendar_sudo:
            calendar_sudo.action_reopen_meeting()
            return request.redirect('/my/meetings')
        return request.render("do_video_conference.portal_my_meeting", values)

    def _get_mandatory_fields(self):
        return ["name", "partner_id"]

    def checkout_form_validate(self, mode, all_form_values, data):
        error = dict()
        error_message = []
        required_fields = self._get_mandatory_fields()
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))
        return error, error_message

    @http.route(['/my/meeting/create'], type='http', auth="user", methods=['GET', 'POST'], website=True, cors='*')
    def portal_my_meeting_create(self, **kwargs):
        calender_id = False
        values, errors = {}, {}
        error_msg = []
        calendar_sudo = request.env['calendar.event'].sudo()
        try:
            if kwargs and kwargs.get('mode') and kwargs.get('mode') == 'create':
                mode = kwargs.get('mode')
                pre_values = {k: v for k, v in values.items()}
                errors, error_msg = self.checkout_form_validate(mode, kwargs, pre_values)
                meeting_values = self.meeting_values(**kwargs)
                calender_id = calendar_sudo.create(meeting_values)
            values.update({'mode': 'create'})
            if calender_id:
                return request.redirect('/my/meetings')
        except Exception as e:
            error_msg.append(str(e))
        errors['error_message'] = error_msg
        values.update({'error': errors})
        values.update(kwargs)
        return request.render("do_video_conference.portal_my_meeting", values)

    @http.route('/meeting/get_tags', type='http', auth="public", methods=['GET'], website=True, sitemap=False)
    def tag_read(self, modal, field_name, query='', domain="[]", limit=25, **post):
        domain = literal_eval(domain)
        domain += [(field_name, 'ilike', (query or ''))]
        data = request.env[modal].sudo().search_read(
            domain=domain,
            fields=['id', field_name],
            limit=int(limit),
        )
        for d in data:
            if d and 'name' not in d.keys():
                d.update({'name': d.get(field_name)})
        return json.dumps(data)
