/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { user } from "@web/core/user";

var AttachmentPreviewMixin = {
	canDocumentPreview: function(extension) {
		return $.inArray(
		extension,
		[
		  'odt', 'odp', 'ods', 'fodt', 'pdf', 'ott', 'fodp', 'otp',
		  'fods', 'ots'
		]) > -1;
	},
	canImagePreview: function(extension) {
		return $.inArray(
			extension,
			[
			  'jpg', 'png', 'gif', 'jpeg', 'bmp', 'ico', 'jfif', 'pjpeg', 'pjp', 'svg', 'tif', 'tiff', 'webp', 'apng', 'cur'
			]
		) > -1;
	},
	canOfficePreview: function(extension) {
		return $.inArray(
			extension,
			[
				'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'txt', 'css', 'html', 'js', 'c', 'cpp', 'mov', 'wmv', 'avi', 'mpeg4'
			]
		) > -1;
	},
	showPreview: function(attachment_id, attachment_url, attachment_extension, attachment_title) {
		if (this.canDocumentPreview(attachment_extension)) {
			var url = (window.location.origin || '') +
			'/do_video_conference/static/lib/ViewerJS/index.html' +
			'?type=' + encodeURIComponent(attachment_extension) +
			'&title=' + encodeURIComponent(attachment_title) +
			'#' +
			attachment_url.replace(window.location.origin, '');
			var $iframe = "<iframe src=" + url + " width='100%' height='500' allowfullscreen webkitallowfullscreen></iframe>";
			$('.attachment_previews').append($iframe);
		}
		else if (this.canImagePreview(attachment_extension)) {
			var $iframe = "<div id='lightgallery'><img src='" + attachment_url.replace(window.location.origin, '') + "' data-src='" + attachment_url.replace(window.location.origin, '') + "' class='img-fluid position-relative m-auto' id='attachment_previews_image' alt='" + attachment_title + "' data-zoom-image='" + attachment_url.replace(window.location.origin, '') + "'/></div>";
			$('.attachment_previews').append($iframe);
			// // $("#attachment_previews_image").ezPlus({scrollZoom: true});
			// $("#lightgallery").lightGallery();
		}
		else if (this.canOfficePreview(attachment_extension)) {
			var url = 'https://docs.google.com/gview' +
			  '?url=' + window.location.origin + attachment_url;
			var $iframe = "<iframe src=" + url + " width='100%' height='500' allowfullscreen webkitallowfullscreen></iframe>";
			$('.attachment_previews').append($iframe);
		}
		else if (attachment_url && attachment_url.indexOf("docs.google.com") >= 0) {
			//&rm=minimal
			var url = attachment_url + '&embedded=true';
			var $iframe = "<iframe src=" + url + " width='100%' height='500' allowfullscreen webkitallowfullscreen></iframe>";
			$('.attachment_previews').append($iframe);
		}
		else {
			var url = attachment_url;
			var $iframe = "<iframe src=" + url + " width='100%' height='500' allowfullscreen webkitallowfullscreen></iframe>";
			$('.attachment_previews').append($iframe);
		}
	}
};

publicWidget.registry.MeetingAttachmentListAdd = publicWidget.Widget.extend(AttachmentPreviewMixin, {
	dependencies: ["bus_service", "notification"],
	selector: '#attachments_list_add',

	events: {
	  'click .button_attachment_add': '_onClickButtonAttachmentAdd',
	  'click .o_sidebar_preview_attachment': '_onPreviewAttachment',
	  'change .file_attachment_type': '_onChangeFileAttachmentType',
	  'click .o_sidebar_attachment_delete': '_onClickButtonAttachmentDelete',
	  'click .o_sidebar_attachment_download': '_onClickButtonAttachmentDownload',
	},

	init: function() {
		this.channel_name = null;
		this.res_id = null;
		this._super.apply(this, arguments);
	},

	start: function() {
		var self = this;
		this.channel_name = this.$el.data('notify_event_channel_name');
		this.res_id = this.$el.data('res_id');
		this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
		this.call('bus_service', 'addChannel', this.channel_name);
		$(".slide-toggle").click(function() {
			$(".attachment_sliding").animate({
				width: "toggle"
			});
			$('.slide_attachment_previews').toggleClass('col-lg-7 col-lg-12');
		});
		$('.perview_full_screen').click(function() {
			$('.main_attachment').toggleClass('col-lg-5 col-lg-12');
			$('.attachment_sliding').toggleClass('col-lg-5 col-lg-2');
			$('.slide_attachment_previews').toggleClass('col-lg-7 col-lg-10 ');
			$('.full_meeting').toggleClass('col-lg-7 col-lg-12');
		});
		var options = {
			alwaysShowResizeHandle: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
			resizable: {
			  handles: 'e, se, s, sw, w'
			},
			disableOneColumnMode: false,
		};
		var grid = GridStack.init(options);
		ClassicEditor.create(document.querySelector('.editor'), {
			toolbar: {
				items: [
					'exportPdf',
					'heading',
					'|',
					'bold',
					'italic',
					'link',
					'bulletedList',
					'numberedList',
					'|',
					'indent',
					'outdent',
					'|',
					'imageUpload',
					'blockQuote',
					'insertTable',
					'mediaEmbed',
					'undo',
					'redo',
					'code',
				]
			},
			language: 'en',
			image: {
				toolbar: [
					'imageTextAlternative',
					'imageStyle:full',
					'imageStyle:side'
				]
			},
			table: {
				contentToolbar: [
					'tableColumn',
					'tableRow',
					'mergeTableCells'
				]
			},
			licenseKey: '',
		}).then(editor => {
			window.editor = editor;
		}).catch(error => {
			console.error('Oops, something gone wrong!');
			console.error('Please, report the following error in the https://github.com/ckeditor/ckeditor5 with the build id and the error stack trace:');
			console.warn('Build id: ae4sx3c3vmh6-jbst2lafi0rx');
			console.error(error);
		});
		$('#button_save_note').click(function(event) {
			event.preventDefault();
			var value = window.editor.getData();
			self.save_note(value);
		});
		return this._super.apply(this, arguments);
	},

	fetchAttachmentList:async function(res_id) {
		var self = this;
		await rpc("/meeting/attachment/fetch",
			{
			 ' res_id': res_id,
			}
		).then(function(data) {
			self._updateAttachmentListView(data['do_video_conference.website_ir_attachment_list']);
		});
	},

	_handleNotification:async function(notification) {
		var self = this;
		if (notification && this.channel_name && (notification[0] === this.channel_name)) {
			if (notification[1].type === 'attachment_added') {
				if (this.res_id) {
					this.fetchAttachmentList(this.res_id);
				}
			}
			if (notification[1].type === 'attendance_manual_entery') {
				if (self.res_id) {
					await rpc("/meeting/get_participant_status",
					{
						'res_id': self.res_id,
					}).then(function(data) {
						$("#participant_section_list").first().before(data['do_video_conference.participant_status_template']).end().remove();
					});
				}
			}
		}
	},

	_onNotification: function(notifications) {
		var self = this;
		$.each(notifications, function(notification) {
			self._handleNotification(notification);
		});
	},

	resetAttachmentForm: function() {
		var self = this;
		$('.form_attachment_add')[0].reset();
	},

	_updateAttachmentListView: function(attachment) {
		// $(".website_ir_attachment_list").first().before(attachment).end().remove();
		$(".website_ir_attachment_list").first().before(attachment).remove();
		return true;
	},

	disableButton: function(button) {
		$(button).attr('disabled', true);
		$(button).prepend('<span class="o_loader"><i class="fa fa-refresh fa-spin"></i>&nbsp;</span>');
	},

	enableButton: function(button) {
		$(button).attr('disabled', false);
		$(button).find('span.o_loader').remove();
	},

	_onClickButtonAttachmentAdd:async function(event) {
		var self = this;
		var $from = this.$target.find('.form_attachment_add');
		var button = event.target;
		this.disableButton(button);
		$from[0].checkValidity();
		$from[0].reportValidity();
		if ($from[0].reportValidity()) {
			this.form_fields = $from.serializeArray();
			$.each($from.find('input[type=file]'), function(outer_index, input) {
				$.each($(input).prop('files'), function(index, file) {
					self.form_fields.push({
						name: input.name + '[' + outer_index + '][' + index + ']',
						value: file
					});
				});
			});
			var form_values = {};
			// $.each(this.form_fields, function(input) {
			//  if (input.name in form_values) {
			//      if (Array.isArray(form_values[input.name])) {
			//          form_values[input.name].push(input.value);
			//      }
			//      else {
			//          form_values[input.name] = [form_values[input.name], input.value];
			//      }
			//  }
			//  else {
			//      if (input.value !== '') {
			//          form_values[input.name] = input.value;
			//      }
			//  }
			// });

			this.form_fields.forEach(function(input) {
				if (input.name in form_values) {
					if (Array.isArray(form_values[input.name])) {
						form_values[input.name].push(input.value);
					} else {
						form_values[input.name] = [form_values[input.name], input.value];
					}
				} else {
					if (input.value !== '') {
						form_values[input.name] = input.value;
					}
				}
			});

			var file = false;
			// map($from.find('input[type=file]')[0].files, function(fi) {
			//  file = fi;
			// });
			Array.from($from.find('input[type=file]')[0].files).map(function(fi) {
				file = fi;
			});

			// var data = {
			// 	'name': form_values.name,
			// 	'file': file,
			// 	'res_id': parseInt(form_values.res_id),
			// 	'res_model': form_values.res_model,
			// 	'type': form_values.type,
			// 	'csrf_token': form_values.csrf_token,
			// 	'public': true,
			// 	'url': form_values.url,
			//   // 'access_token': self.options.token,
			// };

			if (form_values.url) {
				var data = {
					'name': form_values.name,
					// 'file': binaryData,
					// 'filename': file.name,
					'res_id': parseInt(form_values.res_id),
					'res_model': form_values.res_model,
					'type': form_values.type,
					'csrf_token': form_values.csrf_token,
					'public': true,
					'url': form_values.url,
				  // 'access_token': self.options.token,
				};

				await rpc('/meeting/attachment/add',data).then(function (attachmentData) {
				var attachment = attachmentData.response_content
					self.resetAttachmentForm();
					self._updateAttachmentListView(attachment);
					self.enableButton(button);
				});
			} else {
				const reader = new FileReader();
				reader.onload = async function(event) {
					const binaryData = event.target.result;
					var data = {
						'name': form_values.name,
						'file': binaryData,
						'filename': file.name,
						'res_id': parseInt(form_values.res_id),
						'res_model': form_values.res_model,
						'type': form_values.type,
						'csrf_token': form_values.csrf_token,
						'public': true,
						'url': form_values.url,
					  // 'access_token': self.options.token,
					};

					await rpc('/meeting/attachment/add',data).then(function (attachmentData) {
					var attachment = attachmentData.response_content
						self.resetAttachmentForm();
						self._updateAttachmentListView(attachment);
						self.enableButton(button);
					});
				}
				reader.readAsDataURL(file);
				}

			return false;
		}
		return false;
	},

	_SetlogfAttachment:async function(attachment_id, type) {
		var self = this;
		await rpc("/meeting/attachment/log",
			{
				'res_id': self.res_id,
				'attachment_id': parseInt(attachment_id, 10),
				'type': type
			}
		)
	},

	_onPreviewAttachment: function(event) {
		event.preventDefault();
		$('.attachment_previews').empty();
		var self = this,
		$target = $(event.currentTarget),
		attachment_id = parseInt($target.attr('data-id'), 10),
		attachment_url = $target.attr('data-url'),
		attachment_extension = $target.attr('data-extension'),
		attachment_title = $target.attr('data-original-title');

		if (attachment_extension) {
			this._SetlogfAttachment(attachment_id, 'preview');
			this.showPreview(attachment_id, attachment_url, attachment_extension, attachment_title);
		}
	},
	_onChangeFileAttachmentType: function(event) {
		var self = this,
		$target = $(event.currentTarget);
		if ($target.val() === 'url') {
			$('.file_attachment_url').removeClass('d-none');
			$('.file_attachment_binary').addClass('d-none');
		}
		if ($target.val() === 'binary') {
			$('.file_attachment_url').addClass('d-none');
			$('.file_attachment_binary').removeClass('d-none');
		}
	},
	_onClickButtonAttachmentDelete:async function(event) {
		event.preventDefault();
		var self = this,
		$target = $(event.currentTarget);
		var attachment_id = parseInt($target.attr('data-id'), 10);
		await rpc("/meeting/attachment/delete",
			{
				'res_id': self.res_id,
				'attachment_id': attachment_id,
			},
		).then(function (attachmentData) {
			var attachment = attachmentData.response_content
			self.resetAttachmentForm();
			self._updateAttachmentListView(attachment);
		});
		// $.confirm({
		// 	title: 'Delete',
		// 	content: 'Delete ' + $target.attr('data-name') + ' file?',
		// 	icon: 'fa fa-question-circle',
		// 	animation: 'scale',
		// 	closeAnimation: 'scale',
		// 	opacity: 0.5,
		// 	buttons: {
		// 		'confirm': {
		// 			text: 'Proceed',
		// 			btnClass: 'btn-blue',
		// 			action:async function() {
		// 				var attachment_id = parseInt($target.attr('data-id'), 10);
		// 				return await rpc("/meeting/attachment/delete",
		// 					{
		// 						'res_id': self.res_id,
		// 						'attachment_id': attachment_id,
		// 					},
		// 				)
		// 			}
		// 		},
		// 		cancel: function() {},
		// 	}
		// });
		return false;
	},

	save_note:async function(value) {
		var self = this;
		if (value && self.res_id && user.userId) {
			await rpc("/meeting/note/add",
				{
					'res_id': self.res_id,
					'user_id': user.userId,
					'value': value,
				},
			)
		}
	},
	_onClickButtonAttachmentDownload: function(event) {
		event.preventDefault();
		var self = this,
		$target = $(event.currentTarget);
		var attachment_id = parseInt($target.attr('data-id'), 10);
		self._SetlogfAttachment(attachment_id, 'download');
		var url = $target.attr('href');
		location.replace(url);
	},
});