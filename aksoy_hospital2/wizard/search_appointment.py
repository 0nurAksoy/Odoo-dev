# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "Randevu Arama Sihirbazi"

    patient_id = fields.Many2one('hospital.patient', string="Hasta", required=True)

    def action_search_appointment_m1(self):
        action = self.env.ref('aksoy_hospital2.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointment_m2(self):
        action = self.env['ir.actions.actions']._for_xml_id("aksoy_hospital2.action_hospital_appointment")
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointment_m3(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Randevular',
            'res_model': 'hospital.appointment',
            'view_type': 'form',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }



