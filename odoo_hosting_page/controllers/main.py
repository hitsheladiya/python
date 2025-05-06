from odoo import http
from odoo.http import request
import random
import logging

_logger = logging.getLogger(__name__)

class Odoohosting(http.Controller):

    @http.route('/odoo-hosting', type='http', auth="user", website=True, csrf=True)
    def odoo_hosting(self, **post):
        open_model = False
        otp_sent = False
        otp_box_show = False
        otp_verified = False
        error_msg = False
        email = post.get("email")
        restart_timer = False

        lead = request.env['crm.lead'].sudo().search([('email_from', '=', email)], limit=1)

        if post.get("otp_digit_0"):
            if post.get("otp_expired") == "1":
                error_msg = "OTP has expired. Please click 'Resend OTP'."
                otp_box_show = True
                open_model = True
                restart_timer = False  # Don't restart timer
                return request.render("odoo_hosting_page.odoo_hosting_template", {
                    'otp_sent': True,
                    'open_model': open_model,
                    'otp_box_show': otp_box_show,
                    'otp_verified': False,
                    'email': email,
                    'error_msg': error_msg,
                    'restart_timer': restart_timer,
                })

            entered_otp = "".join([
                post.get("otp_digit_0", ""),
                post.get("otp_digit_1", ""),
                post.get("otp_digit_2", ""),
                post.get("otp_digit_3", ""),
            ])

            verified_tag = request.env['crm.tag'].sudo().search([('name', '=', 'Verified')], limit=1)
            if not verified_tag:
                verified_tag = request.env['crm.tag'].sudo().create({'name': 'Verified'})

            not_verified_tag = request.env['crm.tag'].sudo().search([('name', '=', 'Not Verified')], limit=1)
            if not not_verified_tag:
                not_verified_tag = request.env['crm.tag'].sudo().create({'name': 'Not Verified'})

            if lead and lead.otp == entered_otp:
                otp_verified = True
                otp_box_show = False
                open_model = True
                lead.write({'tag_ids': [(6, 0, [verified_tag.id])]})
                restart_timer = False
            else:
                error_msg = "OTP invalid. Please resend OTP."
                otp_box_show = True
                open_model = True
                restart_timer = False
                if lead:
                    lead.write({'tag_ids': [(6, 0, [not_verified_tag.id])]})

        elif post.get("send_otp") and email:
            restart_timer = True
            otp = ''.join(str(random.randint(0, 9)) for _ in range(4))
            request.session['email_otp'] = otp
            request.session['email_otp_address'] = email
            open_model = True
            otp_sent = True
            otp_box_show = True

            selected_plan = post.get("plan", "")
            if lead:
                lead.write({'otp': otp, 'selected_plan': selected_plan})
            else:
                lead = request.env['crm.lead'].sudo().create({
                    'name': f'Verification Lead - {email}',
                    'email_from': email,
                    'otp': otp,
                    'selected_plan': selected_plan,
                })

            try:
                mail_values = {
                    'subject': 'Your OTP for Verification',
                    'body_html': f'<p>Your verification OTP is: <strong>{otp}</strong></p>',
                    'email_to': email,
                    'email_from': request.env.user.email or 'hitsheladiyya08@gmail.com',
                }
                mail = request.env['mail.mail'].sudo().create(mail_values)
                mail.send()
            except Exception as e:
                _logger.error(f"Failed to send OTP email: {str(e)}")
                error_msg = "Failed to send OTP. Please try again."

        # ----- Case: Resend OTP -----
        elif post.get("resend_otp") and email:
            restart_timer = True
            otp = ''.join(str(random.randint(0, 9)) for _ in range(4))
            request.session['email_otp'] = otp
            request.session['email_otp_address'] = email
            open_model = True
            otp_sent = True
            otp_box_show = True

            if lead:
                lead.write({'otp': otp})
                try:
                    mail_values = {
                        'subject': 'Your New OTP for Verification',
                        'body_html': f'<p>Your new verification OTP is: <strong>{otp}</strong></p>',
                        'email_to': email,
                        'email_from': request.env.user.email or 'hitsheladiyya08@gmail.com',
                    }
                    mail = request.env['mail.mail'].sudo().create(mail_values)
                    mail.send()
                except Exception as e:
                    _logger.error(f"Failed to resend OTP email: {str(e)}")
                    error_msg = "Failed to resend OTP. Please try again."

        return request.render("odoo_hosting_page.odoo_hosting_template", {
            'otp_sent': otp_sent,
            'open_model': open_model,
            'otp_box_show': otp_box_show,
            'otp_verified': otp_verified,
            'email': email,
            'error_msg': error_msg,
            'restart_timer': restart_timer,
        })