# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'convert a lead in crm to a project'

    project_id = fields.Many2one('project.project', string='Project', ondelete='set null')

    def action_convert_to_a_project(self):
        self.ensure_one()
        self.convert_to_a_project()
        # if self.stage_id.id == 4:
        #     self.convert_to_a_project()
        # else:
        #     raise Warning("You can just convert a sale's lead to a project when it wins.")

        return True

    def convert_to_a_project(self):
        _logger.info("start to convert into a project!")
        for lead in self:
            _logger.info(lead.project_id.id)
            if not lead.project_id.id:
                project = self.env['project.project'].create({
                    'name': lead.name + " (from CRM)",
                    'description': "This project is converted from a sale's lead (" + lead.name + ")",
                    'company_id': lead.company_id.id,
                    'partner_id': lead.partner_id.id,
                    'lead_id': lead.id,
                    'active': True,
                })
                lead.write({'project_id': project.id})
            else:
                raise Warning("The project has been created as \"" + lead.name + " (from CRM)\".")
        _logger.info("finish converting into a project!")
        return True


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'convert a lead in crm to a task in project'

    lead_id = fields.Many2one('crm.lead', string='Sale''s Lead', ondelete='set null')
