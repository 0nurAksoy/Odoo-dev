# -*- coding: utf-8 -*-
{
    'name': 'Hastane Yonetimi',
    'version': '1.0.0',
    'summary': 'Basit Hastane Yonetimi',
    'sequence': -115,
    'description': """Basit Hastane Yonetimi""",
    'category': 'Hastane',
    'author': 'Onur Aksoy',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'mail',
        'website_slides',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',

        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',

        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/sale.xml',

        'report/patient_details_template.xml',
        'report/patient_card.xml',
        'report/report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
