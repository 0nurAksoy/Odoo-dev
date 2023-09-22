# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Doktorlar"
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Isim', required=True, tracking=True)
    date_of_birth = fields.Date(string='Dogum Tarihi')
    age = fields.Integer(string='Yas', tracking=True, compute='_compute_age')
    gender = fields.Selection([
        ('male', 'Erkek'),
        ('female', 'Kadin'),
        ('other', 'Diger'),
    ], required=True, default='male', tracking=True)
    branch = fields.Selection([
        ('pediatrics', 'Pediatri'),
        ('dermatology', 'Dermatoloji'),
        ('internal', 'Dahiliye'),
        ('cardiology', 'Kardiyoloji'),
        ('neurology', 'Nöroloji'),
        ('radiology', 'Radyoloji'),
        ('psychiatry', 'Psikiyatri'),
        ('general', 'Genel Cerrahi'),
        ('orthopedics', 'Ortopedi'),
        ('male', 'Erkek'),
        ('female', 'Kadin'),
        ('other', 'Diger'),
    ], required=True, tracking=True)

    note = fields.Text(string='Not')
    image = fields.Binary(string="Doktor Resim")
    appointment_count = fields.Integer(string='Randevu Sayisi', compute='_compute_appointment_count')
    active = fields.Boolean(string="Aktif", default=True)

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)", self.doctor_name)
        default['note'] = "Copied Record"
        return super(HospitalDoctor, self).copy(default)

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1
