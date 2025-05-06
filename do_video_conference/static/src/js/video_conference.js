/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.VideoConference = publicWidget.Widget.extend({
    selector: '#meeting',
    jsLibs: [
        'https://meet.jit.si/external_api.js',
        'https://code.jquery.com/jquery-3.6.0.min.js',
    ],
    events: {},
    /**
     * @constructor
     */
    init: function() {
        this._super.apply(this, arguments);
    },

    start: function () {
        var self = this;
        self.user_id = session.user_id;
        self.jitsi_data = $(this.selector).data();
        self.calendar_event_id = self.jitsi_data.calendar_event_id;
        $('.presence_meeting').click(function(event) {
            var is_otp_enable = $(event.currentTarget).data('otp-enable');
            if (is_otp_enable) {
                // await rpc("/meeting/send_otp",{ 'res_id': self.calendar_event_id }).then(function(data) {
                //  $('#email_otp_model').modal();
                // });
                self._send_otp()
            }
            else {
                if ($('.jitsi_meeting').length == 1) {
                    self._loadJITSIMeeting().then(function() {
                        self.onClickPresenceMeeting(event);
                    });
                }
                else {
                    self.onClickPresenceMeeting(event);
                }
            }
        });
        $('.otp_model_submit').click(function(event) {
            $('.otp_error_meesage').empty();
            var otp_input = $('#otp_input').val();
            self._verify_otp(otp_input)
        });
        $('.otp_model_close').click(function(event) {
            $('#email_otp_model').css('opacity', '0');
            $('#email_otp_model').css('display', 'none')
        });
        $('.leave_meeting').click(function(event) {
            self.onClickLeaveMeeting(event);
        });

        if ($('.jitsi_meeting').length == 1 && $('.jitsi_already_checked_in').length == 1) {
            self._loadJITSIMeeting().then(function() {
                self.onClickPresenceMeeting(event);
            });
        }

        window.onbeforeunload = function (event) {
            self.onClickLeaveMeeting();
            return;
        };
        return this._super.apply(this, arguments);
    },

    _send_otp:async function() {
        await rpc("/meeting/send_otp",{ 'res_id': this.calendar_event_id }).then(function(data) {
            $('#email_otp_model').css('opacity', '1');
            $('#email_otp_model').css('display', 'block')
        });
    },

    _verify_otp:async function(otp_input) {
        self = this;
        await rpc("/meeting/verify_otp", {
            'res_id': this.calendar_event_id,
            'otp': otp_input,
        }).then(function(data) {
            if (data.error) {
                $('.otp_error_meesage').removeClass('d-none');
                $('.otp_error_meesage').append("<strong>" + data.error + "</strong>")
            }
            else {
                if ($('.jitsi_meeting').length == 1) {
                    self._loadJITSIMeeting().then(function() {
                        self.onClickPresenceMeeting(event);
                    });
                }
                else {
                    self.onClickPresenceMeeting(event);
                }
                $('#email_otp_model').css('opacity', '0');
                $('#email_otp_model').css('display', 'none');
            }
        });
    },

    _loadJITSIMeeting: function() {
        var self = this;
        self.jitsi_data = $(this.selector).data();
        var jitsi_password = self.jitsi_data.password
        var domain = self.jitsi_data.domain || 'meet.jit.si';
        var requireDisplayName = false;
        var DEFAULT_REMOTE_DISPLAY_NAME = 'Undefined'
        if (session.is_website_user) {
            requireDisplayName = true;
        } else {
            DEFAULT_REMOTE_DISPLAY_NAME = self.jitsi_data.username;
        }
        var options = {
            roomName: self.jitsi_data.roomname,
            width: '100%',
            height: '500px',
            parentNode: document.querySelector(this.selector),
            configOverwrite: {
                enableUserRolesBasedOnToken: true,
                requireDisplayName: requireDisplayName,
            },
            interfaceConfigOverwrite: {
                DEFAULT_REMOTE_DISPLAY_NAME: DEFAULT_REMOTE_DISPLAY_NAME,
                DEFAULT_LOCAL_DISPLAY_NAME: 'me',
                SHOW_JITSI_WATERMARK: false,
                JITSI_WATERMARK_LINK: '',
                SHOW_WATERMARK_FOR_GUESTS: false,
                SHOW_BRAND_WATERMARK: false,
                BRAND_WATERMARK_LINK: '',
                SHOW_POWERED_BY: false,
                SHOW_DEEP_LINKING_IMAGE: false,
                GENERATE_ROOMNAMES_ON_WELCOME_PAGE: true,
                DISPLAY_WELCOME_PAGE_CONTENT: true,
                DISPLAY_WELCOME_PAGE_TOOLBAR_ADDITIONAL_CONTENT: false,
                APP_NAME: 'Jitsi Meet',
                NATIVE_APP_NAME: 'Jitsi Meet',
                PROVIDER_NAME: 'Jitsi',
                LANG_DETECTION: true,
                INVITATION_POWERED_BY: true,
                DISABLE_TRANSCRIPTION_SUBTITLES: false,
                CLOSE_PAGE_GUEST_HINT: true,
                SHOW_PROMOTIONAL_CLOSE_PAGE: true,
            },
            userInfo: {
                email: self.jitsi_data.partner_emails,
                displayName: self.jitsi_data.partner_name,
            }
        }
        if (!self.jitsi_data.chat_jitsi) {
            options.interfaceConfigOverwrite['TOOLBAR_BUTTONS'] = [
                'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
                'fodeviceselection', 'hangup', 'profile', 'recording',
                'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
                'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
                'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone',
                'e2ee', 'security'
            ]
        }
        var custJitsiAPI = new JitsiMeetExternalAPI(domain, options);
        if (jitsi_password) {
            custJitsiAPI.addEventListener('participantRoleChanged', function(event) {
                // when host has joined the video conference
                if (event.role == 'moderator') {
                    custJitsiAPI.executeCommand('password', jitsi_password);
                }
                else {
                    setTimeout(() => {
                        // why timeout: I got some trouble calling event listeners without setting a timeout :)

                        // when local user is trying to enter in a locked room
                        custJitsiAPI.addEventListener('passwordRequired', () => {
                            custJitsiAPI.executeCommand('password', jitsi_password);
                        });

                        // when local user has joined the video conference
                        custJitsiAPI.addEventListener('videoConferenceJoined', (response) => {
                            setTimeout(function() { custJitsiAPI.executeCommand('password', jitsi_password); }, 300);
                        });

                    }, 10);
                }
            });
        }

        custJitsiAPI.addEventListener('participantJoined', function(response) {
            self.onparticipantJoined(response);
        });
        custJitsiAPI.addEventListener('participantKickedOut', function(response) {
            self.onParticipantKickedOut(response);
        });
        custJitsiAPI.addEventListener('participantLeft', function(response) {
            self.onParticipantLeft(response);
        });
        custJitsiAPI.addEventListener('videoConferenceJoined', function(response) {
            self.onVideoConferenceJoined(response);
        });
        custJitsiAPI.addEventListener('videoConferenceLeft', function(response) {
            self.onVideoConferenceLeft(response);
        });
        custJitsiAPI.addEventListener('readyToClose', function(response) {
            self.onReadyToClose(response);
        });
        custJitsiAPI.addEventListener('incomingMessage', function(response) {
            self.onReadyToClose(response);
        });
        custJitsiAPI.addEventListener('outgoingMessage', function(response) {
            self.onOutgoingMessage(response);
        });
        self.custJitsiAPI = custJitsiAPI;
        return $.when();
    },

    onGetParticipantStatus:async function() {
        var self = this;
        await rpc('/meeting/get_participant_status',{               
            'res_id': self.calendar_event_id
        }).then(function(data) {
            $("#participant_section_list").first().before(data['do_video_conference.participant_status_template']).end().remove();
        });
    },

    onparticipantJoined: function(object) {
        var self = this;
        setTimeout(function() { self.onGetParticipantStatus(); }, 3000);
    },

    onParticipantKickedOut: function(object) {
        var self = this;
        setTimeout(function() { self.onGetParticipantStatus(); }, 3000);
    },

    onParticipantLeft: function(object) {
      var self = this;
      setTimeout(function() { self.onGetParticipantStatus(); }, 3000);
    },

    onVideoConferenceJoined: function(object) {
        var self = this;
        self.jitsi_id = object.id;
        self.onGetParticipantStatus();
    },

    onVideoConferenceLeft: function(object) {
        var self = this;
        self.onGetParticipantStatus();
    },

    onReadyToClose: function(object) {
        var self = this;
        self.onGetParticipantStatus();
    },

    onOutgoingMessage:async function(object) {
        var self = this;
        await rpc('/calendar_event/log_outgoing_message',{ 'calendar_id':self.calendar_event_id,'message':object.message})
        // this._rpc({
        //  model: 'calendar.event',
        //  method: 'log_outgoing_message',
        //  args: [
        //      [self.calendar_event_id], object.message
        //  ],
        // });
    },

    disableButton: function(button) {
        $(button).attr('disabled', true);
        $(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');
    },

    enableButton: function(button) {
        $(button).attr('disabled', false);
        $(button).find('span.o_loader').remove();
    },

    onClickPresenceMeeting:async function(event) {
        var self = this;
        if (event) {
            var button = event.target;
        }
        if (button) {
            this.disableButton(button);
        }
        $('.bbb_password_error_meesage').html('');
        // $('#bbbPasswordModal').modal({backdrop: 'static', keyboard: false});
        $('#bbbPasswordModal').css('opacity', '1');
        $('#bbbPasswordModal').css('display', 'block');
        $('.modal-backdrop.show').css('opacity', '1');
        $('#bigbluebutton_passwordcheck').click(async function(){
            var password = $('#bbb_attendeepassword_input').val();
            if(password && self.calendar_event_id){
                await rpc("/meeting/bbb_password_check",{
                    'res_id': self.calendar_event_id,
                    'password': password,                   
                }).then(function(data) {
                    if (data && data.error) {
                        $('.bbb_password_error_meesage').removeClass('d-none');
                        $('.bbb_password_error_meesage').append("<strong>" + data.error + "</strong>");
                    } else {
                        $('#bbbPasswordModal').hide();
                        if(data && data.bbb_join_url){
                            $("iframe#meeting").attr('src', data.bbb_join_url)
                        }
                        // if(data && data.bbb_attendee){
                        //   var bbb_attendee = true;
                        // }
                        // if(data && data.bbb_moderator){
                        //   var bbb_moderator = true;
                        // }
                    }
                });
                // self._rpc({
                //  url: "/meeting/bbb_password_check",
                //  params: {
                //      res_id: self.calendar_event_id,
                //      password: password,
                //  },
                // }).then(function(data) {
                //  if (data && data.error) {
                //      $('.bbb_password_error_meesage').removeClass('d-none');
                //      $('.bbb_password_error_meesage').append("<strong>" + data.error + "</strong>");
                //  } else {
                //      $('#bbbPasswordModal').modal('hide');
                //      if(data && data.bbb_join_url){
                //          $("iframe#meeting").attr('src', data.bbb_join_url)
                //      }
                //      // if(data && data.bbb_attendee){
                //      //   var bbb_attendee = true;
                //      // }
                //      // if(data && data.bbb_moderator){
                //      //   var bbb_moderator = true;
                //      // }
                //  }
                // });
            }
            else
            {
                $('.bbb_password_error_meesage').html('<span>Password Not valid</span>');
            }
        });
        
        if (self.jitsi_data && self.jitsi_data.partner_id) {            
            await rpc('/calendar_event/attendance_manual_entery',{              
                'calendar_id': self.calendar_event_id,
                'partner_id': self.jitsi_data.partner_id,
                'type': 'checked_in',
            })
            
            await rpc('/calendar_event/attendance_manual_entery',{              
                'calendar_id': self.calendar_event_id,
                'partner_id': self.jitsi_data.partner_id,
                'type': 'checked_in',
            }).then(function(data) {
                self.onGetParticipantStatus();
                $('.leave_meeting').show();
                $('.presence_meeting').hide();
                $('.checked_in_d_none').addClass('checked_out_d_none');
                $('.checked_in_d_none').removeClass('checked_in_d_none');
                $('.full_meeting').removeClass('div_center');
                $('.participant_grid_stack_item').removeClass('participant_grid_stack_item_show');
                $('.grid-stack').removeClass('height_500');
                if (button) {
                    self.enableButton(button);
                }
            });

        }
        else {
            self.displayNotification({
                type: 'warning',
                title: _t("Warning"),
                message: "Video conference is not loaded",
                sticky: false,
            });
            self.enableButton(button);
        }
    },

    onClickLeaveMeeting:async function(event) {
        var self = this;
        if(event){
            var button = event.target;
            this.disableButton(button);
        }
        if (self.jitsi_data && self.jitsi_data.partner_id) {
            await rpc('/calendar_event/attendance_manual_entery',{              
                'calendar_id': self.calendar_event_id,
                'partner_id': self.jitsi_data.partner_id,
                'type': 'checked_out',
            }).then(function(data) {
                self.onGetParticipantStatus();
                $('.leave_meeting').hide();
                $('.presence_meeting').show();
                $('#meeting').find('iframe').remove();
                $('.checked_out_d_none').addClass('checked_in_d_none');
                $('.checked_out_d_none').removeClass('checked_out_d_none');
                $('.full_meeting').addClass('div_center');
                $('.participant_grid_stack_item').addClass('participant_grid_stack_item_show');
                $('.grid-stack').addClass('height_500');
                self.enableButton(button);
            });
            // self._rpc({
            //  model: 'calendar.event',
            //  method: 'attendance_manual_entery',
            //  args: [
            //      [self.calendar_event_id], self.jitsi_data.partner_id, 'checked_out'
            //  ],
            // }).then(function(data) {
            //  self.onGetParticipantStatus();
            //  $('.leave_meeting').hide();
            //  $('.presence_meeting').show();
            //  $('#meeting').find('iframe').remove();
            //  $('.checked_out_d_none').addClass('checked_in_d_none');
            //  $('.checked_out_d_none').removeClass('checked_out_d_none');
            //  $('.full_meeting').addClass('div_center');
            //  $('.participant_grid_stack_item').addClass('participant_grid_stack_item_show');
            //  $('.grid-stack').addClass('height_500');
            //  self.enableButton(button);
            // });
        }
        else {
            self.displayNotification({
                type: 'warning',
                title: _t("Warning"),
                message: "Video conference is not loaded",
                sticky: false,
            });
            self.enableButton(button);
        }
    },
});