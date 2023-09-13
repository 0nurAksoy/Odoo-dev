# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '2.0.0',
    'summary': 'Basic Hospital Management',
    'sequence': -100,
    'description': """Basic Hospital Management""",
    'category': 'Hospital',
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

        'data/patient_tag_data.xml',
        'data/patient_tag.csv',

        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',

        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/kids_view.xml',
        'views/patient_tag_view.xml',
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
