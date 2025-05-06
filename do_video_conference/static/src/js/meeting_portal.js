/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { addLoadingEffect } from '@web/core/utils/ui';

publicWidget.registry.meetingPortalDetails = publicWidget.Widget.extend({
    selector: '.o_portal_meeting_details',
    events: {
        'change select[name="conference_type"]': '_onVideoConferenceType',
        'change .meeting_input_checkbox': '_onMeetingInputCheckbox',
    },
    start: function() {
        var self = this;
        var def = this._super.apply(this, arguments);
        $('#participant_history_ids').DataTable();
        $('#notes_ids').DataTable();
        $('#attachment_history_ids').DataTable();
        $('input.js_select2').each(function() {
            var select = this;
            var id = $(select).attr('id');
            $('#' + id).select2({
                tags: true,
                tokenSeparators: [',', ' ', '_'],
                maximumInputLength: 35,
                minimumInputLength: 2,
                maximumSelectionSize: 5,
                lastsearch: [],
                formatResult: function(term) {
                    if (term.isNew) {
                        return '<span class="badge badge-primary">New</span> ' + CSS.escape(term.text);
                    } else {
                        return CSS.escape(term.text);
                    }
                },
                ajax: {
                    url: '/meeting/get_tags',
                    dataType: 'json',
                    data: function(term) {
                        var domain = $(select).data('domain') || [];
                        return {
                            modal: $(this).data('modal'),
                            field_name: $(select).data('field-name'),
                            query: term,
                            domain: domain,
                            limit: 50,
                        };
                    },
                    results: function(data) {
                        var ret = [];
                        data.forEach(function(x) {
                            ret.push({
                                id: x.id,
                                text: x.name,
                                isNew: false,
                            });
                        });
                        self.lastsearch = ret;
                        return { results: ret };
                    }
                },
                // Take default tags from the input value
                initSelection: function(element, callback) {
                    var data = [];
                    var field_name = $(element).data('field-name');
                    var initValue = $(element).data('init-value');
                    if (Array.isArray(initValue)) {
                        initValue.forEach(function(x) {
                            data.push({ id: x.id, text: x.name, isNew: false });
                        });
                    }
                    // $(element).data('init-value').each(function() {
                    //     var x = this;
                    //     data.push({ id: x.id, text: x.name, isNew: false });
                    // });
                    $(element).val('');
                    callback(data);
                },
            });
        });
        this._adaptVideoConferenceType();
        $('.meeting_input_checkbox').each(function() {
            var event = this
            self._onMeetingInputCheckbox(event);
        })
        return def;
    },
    _adaptVideoConferenceType: function() {
        var $conference_type = this.$('select[name="conference_type"]').val();
        if ($conference_type && $conference_type == 'bigbluebutton') {
            $('.field_do_video_conference').addClass('d-none');
            $('.field_bbb_video_conference').removeClass('d-none');
            $('#bbb_meeting_id').attr('required', 'required');
            $('#bbb_attendeePW').attr('required', 'required');
            $('#bbb_moderatorPW').attr('required', 'required');
        }
        if ($conference_type && $conference_type == 'jitsi') {
            $('.field_do_video_conference').removeClass('d-none');
            $('.field_bbb_video_conference').addClass('d-none');
            $('#bbb_meeting_id').removeAttr('required');
            $('#bbb_attendeePW').removeAttr('required');
            $('#bbb_moderatorPW').removeAttr('required');
        }
    },
    _onVideoConferenceType: function() {
        this._adaptVideoConferenceType();
    },
    _onMeetingInputCheckbox: function(event) {
        var hide_checked = []
        if (event.target) {
            var hide_checked = $(event.target).data('hide-checked');
            if (hide_checked) {
                hide_checked = hide_checked.split(',');
                if ($(event.target).is(':checked')) {
                    hide_checked.forEach(function(input_id) {
                        $('#' + input_id).closest('.form-row').removeClass('d-none');
                    });
                } else {
                    hide_checked.forEach(function(input_id) {
                        $('#' + input_id).closest('.form-row').addClass('d-none');
                    });
                }
            }
        } else {
            if (event && event.dataset) {
                var hide_checked = event.dataset.hideChecked;
                if (hide_checked) {
                    hide_checked = hide_checked.split(',');
                    if ($(event).is(':checked')) {
                        hide_checked.forEach(function(input_id) {
                            $('#' + input_id).closest('.form-row').removeClass('d-none');
                        });
                    } else {
                        hide_checked.forEach(function(input_id) {
                            $('#' + input_id).closest('.form-row').addClass('d-none');
                        });
                    }
                }
            }
        }

    },
});

export default publicWidget.registry.meetingPortalDetails;