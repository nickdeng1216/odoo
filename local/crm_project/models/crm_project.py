# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
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
                    'description': "This project is converted from an opportunity (" + lead.name + ")",
                    'company_id': lead.company_id.id,
                    'partner_id': lead.partner_id.id,
                    'lead_id': lead.id,
                    'active': True,
                })
                lead.write({'project_id': project.id})
            else:
                raise Warning("The project has been created as \"%s (from CRM)\"." % lead.name)
        _logger.info("finish converting into a project!")
        return True

    def write(self, vals):
        _logger.info('start to crm write')
        self.ensure_one()
        lead_id = self.id
        current_project_id = vals.get('project_id')
        pre_project_id = self.project_id.id
        _logger.info('pre_project_id = %s' % pre_project_id)
        _logger.info('current_project_id = %s' % current_project_id)
        _logger.info('lead_id = %s' % lead_id)
        model_project_project = self.env['project.project']
        # if current_project_id is not False:
        #     model_project_project.browse(current_project_id).write({'lead_id': lead_id})
        #     if pre_project_id is not False:
        #         model_project_project.browse(pre_project_id).write({'lead_id': False})
        # else:
        #     if pre_project_id is not False:
        #         model_project_project.browse(pre_project_id).write({'lead_id': lead_id})
        if current_project_id is not False:
            model_project_project.browse(current_project_id).write_from_crm(lead_id)
            if pre_project_id is not False:
                model_project_project.browse(pre_project_id).write_from_crm(False)
        else:
            if pre_project_id is not False:
                model_project_project.browse(pre_project_id).write_from_crm(lead_id)

        super(CrmLead, self).write(vals)

    def write_from_project(self, project_id):
        super(CrmLead, self).write({'project_id': project_id})


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'convert a lead in crm to a task in project'

    lead_id = fields.Many2one('crm.lead', string='Opportunity', ondelete='set null')

    def write(self, vals):
        _logger.info('start to project write')
        self.ensure_one()
        project_id = self.id
        current_lead_id = vals.get('lead_id')
        pre_lead_id = self.lead_id.id
        _logger.info(current_lead_id)
        model_crm_lead = self.env['crm.lead']
        # if current_lead_id is not False:
        #     model_crm_lead.browse(current_lead_id).write({'project_id': project_id})
        #     if pre_lead_id is not False:
        #         model_crm_lead.browse(pre_lead_id).write({'project_id': False})
        # else:
        #     if pre_lead_id is not False:
        #         model_crm_lead.browse(pre_lead_id).write({'project_id': project_id})
        if current_lead_id is not False:
            model_crm_lead.browse(current_lead_id).write_from_project(project_id)
            if pre_lead_id is not False:
                model_crm_lead.browse(pre_lead_id).write_from_project(False)
        else:
            if pre_lead_id is not False:
                model_crm_lead.browse(pre_lead_id).write_from_project(project_id)
        super(Project, self).write(vals)

        # check if there is an existing opportunity connecting to this project
        # domain = [('project_id', '=', project_id)]
        # leads = model_crm_lead.search(domain)
        # leads.browse(pre_lead_id).write({'project_id': project_id})
        # if current_lead_id is False or len(leads) == 0:
        #     super(Project, self).write(vals)
        #     if len(leads) == 0:
        #         lead = model_crm_lead.browse(current_lead_id)
        #         lead.write({'project_id': project_id})
        # else:
        #     _logger.info(leads[0].name)
        #     raise UserError("The project has been connected to %s, please remove the connection in crm first." %
        #                     leads[0].name)
        return True

    def write_from_crm(self, lead_id):
        super(Project, self).write({'lead_id': lead_id})
