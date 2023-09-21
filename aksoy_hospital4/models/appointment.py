# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Randevular"
    _order = "doctor_id,name,age"

    name = fields.Char(string='Sira Sayisi', required=True, copy=False, readonly=True,
                       default=lambda self: _('H'))
    patient_id = fields.Many2one('hospital.patient', string="Hasta Adi", required=True)
    age = fields.Integer(string='Yas', related='patient_id.age', tracking=True, store=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doktor", required=True)
    gender = fields.Selection([
        ('male', 'Erkek'),
        ('female', 'Kadin'),
        ('other', 'Diger'),
    ], string="Cinsiyet")
    state = fields.Selection([('draft', 'Taslak'), ('confirm', 'Dogrulandi'),
                              ('done', 'Tamanlandi'), ('cancel', 'Iptal')], default='draft',
                             string="Durum", tracking=True)
    priority = fields.Selection([
        ('0', 'Dusuk'),
        ('1', 'Normal'),
        ('2', 'Yuksek'),
        ('3', 'Cok Yuksek')], string="Oncelik")
    note = fields.Text(string='Not')
    date_appointment = fields.Date(string="Tarih")
    date_checkup = fields.Datetime(string="Kontrol Tarihi")
    prescription = fields.Text(string="Doktor Gorusleri")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Ilac Listesi")

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    #     return super(HospitalAppointment, self).create(vals)


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''

    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("%s Tamamlandigindan, silemezsiniz !" % self.name))
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://enabiz.gov.tr'
        }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Many2one('product.template', string="Ilac", required=True)
    qty = fields.Integer(string="Sayi")
    appointment_id = fields.Many2one('hospital.appointment', string="Randevu")

