# controllers/main.py
from odoo import http

class ClinicWebsite(http.Controller):
    @http.route('/', auth='public', website=True)
    def homepage(self, **kw):
        return http.request.render('royal_clinic_theme.homepage_dental')

    @http.route('/our-team', type='http', auth='public', website=True)
    def our_team(self):
        doctors = [
                    {
                        'name': 'Dr. John Smith',
                        'specialization': 'General Dentist',
                        'description': 'Experienced in preventive, restorative, and cosmetic dental care with 10+ years of experience.',
                        'image': '/royal_clinic_theme/static/src/image/doctor1.jpg',
                    },
                    {
                        'name': 'Dr. Alice Brown',
                        'specialization': 'Periodontist',
                        'description': 'Specialist in gum treatment, dental implants, and advanced periodontal care with a gentle approach.',
                        'image': '/royal_clinic_theme/static/src/image/doctor2.jpeg',
                    },
                    {
                        'name': 'Dr. Emily Davis',
                        'specialization': 'Endodontist',
                        'description': 'Expert in root canal treatment, dental trauma management, and pain-free endodontic procedures.',
                        'image': '/royal_clinic_theme/static/src/image/doctor3.avif',
                    },
                    {
                        'name': 'Dr. David Lee',
                        'specialization': 'Orthodontist',
                        'description': 'Specialist in teeth alignment, braces, and clear aligner treatments for all age groups.',
                        'image': '/royal_clinic_theme/static/src/image/doctor4.jpg',
                    },
                    {
                        'name': 'Dr. Sophia Green',
                        'specialization': 'Prosthodontist',
                        'description': 'Expert in dental prosthetics, crowns, bridges, and full-mouth rehabilitation.',
                        'image': '/royal_clinic_theme/static/src/image/doctor5.jpg',
                    },
                    {
                        'name': 'Dr. Michael Carter',
                        'specialization': 'Pediatric Dentist',
                        'description': 'Focused on child dental care, early cavity prevention, and child-friendly treatment approaches.',
                        'image': '/royal_clinic_theme/static/src/image/doctor6.avif',
                    },
                ]
        return http.request.render('royal_clinic_theme.our_team_template', {'doctors': doctors})

    @http.route('/about-us', type='http', auth='public', website=True)
    def about_us(self):
        return http.request.render('royal_clinic_theme.about_us_template')

    @http.route('/contact', type='http', auth='public', website=True)
    def contact(self):
        return http.request.render('royal_clinic_theme.contact_template')

    @http.route(['/for-patients'], type='http', auth='public', website=True)
    def for_patients(self):
        return http.request.render('royal_clinic_theme.for_patients_template')

    @http.route('/contact/submit', type='http', auth='public', website=True, csrf=True, methods=['POST'])
    def contact_form_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        message = post.get('message')

        http.request.env['mail.mail'].sudo().create({
            'subject': f'New Message from {name}',
            'email_from': email,
            'email_to': 'clinic@example.com',
            'body_html': f"<p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong><br/>{message}</p>"
        }).send()

        return http.request.render('royal_clinic_theme.thank_you_template')

