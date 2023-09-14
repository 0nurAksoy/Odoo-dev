# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hastalar"
    _order = "id desc"

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['note'] = 'Yeni hasta kaydi'
        return res

    name = fields.Char(string='Isim', required=True, tracking=True)
    reference = fields.Char(string='Sira Sayisi', required=True, copy=False, readonly=True,
                            default=lambda self: _('H'))
    age = fields.Integer(string='Yas', tracking=True)
    gender = fields.Selection([
        ('male', 'Erkek'),
        ('female', 'Kadin'),
        ('other', 'Diger'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Not')
    state = fields.Selection([('draft', 'Taslak'), ('confirm', 'Dogrulandi'),
                              ('done', 'Tamamlandi'), ('cancel', 'Iptal')], default='draft',
                             string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Sorumlu")
    appointment_count = fields.Integer(string='Randevu Sayisi', compute='_compute_appointment_count')
    image = fields.Binary(string="Hasta Fotografi")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Randevular")

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'Yeni hasta'
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Isim %s zaten var!" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Yas degeri 0(sifir) olamaz .. !"))

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
