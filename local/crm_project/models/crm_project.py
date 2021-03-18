# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'convert a lead in crm to a project'

    project_id = fields.Many2one('project.project', string='Project', ondelete='set null')

    # project_ids = fields.Many2many('project.project', string='change log')
    # project_ids = fields.Many2many(
    #     'project.project',
    #     'crm_lead_project_project_rel',
    #     'id',
    #     'id',
    #     'change log')

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
        model_project_project = self.env['project.project']
        if current_project_id is not False:
            model_project_project.browse(current_project_id).write_from_crm(lead_id)
            if pre_project_id is not False:
                model_project_project.browse(pre_project_id).write_from_crm(False)
        else:
            if pre_project_id is not False:
                model_project_project.browse(pre_project_id).write_from_crm(lead_id)

        self.write_lead_project_log(current_project_id, lead_id, self._name)
        super(CrmLead, self).write(vals)

    def write_lead_project_log(self, current_project_id, lead_id, model_name):
        _logger.info('current_project_id=%s' % current_project_id)
        _logger.info('lead_id=%s' % lead_id)
        self.env['crm.lead.project.project.log'].create({
            'lead_id': lead_id,
            'project_id': current_project_id,
            'model_name': model_name,
        })

    def write_from_project(self, project_id):
        super(CrmLead, self).write({'project_id': project_id})


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'convert a lead in crm to a task in project'

    lead_id = fields.Many2one('crm.lead', string='Opportunity', ondelete='set null')

    # lead_ids = fields.Many2many('crm.lead', string='change log')
    # lead_ids = fields.Many2many(
    #     'crm.lead',
    #     'crm_lead_project_project_rel',
    #     'id',
    #     'id',
    #     'change log')

    def write(self, vals):
        _logger.info('start to project write')
        self.ensure_one()
        project_id = self.id
        current_lead_id = vals.get('lead_id')
        pre_lead_id = self.lead_id.id
        model_crm_lead = self.env['crm.lead']
        if current_lead_id is not False:
            model_crm_lead.browse(current_lead_id).write_from_project(project_id)
            if pre_lead_id is not False:
                model_crm_lead.browse(pre_lead_id).write_from_project(False)
        else:
            if pre_lead_id is not False:
                model_crm_lead.browse(pre_lead_id).write_from_project(project_id)

        self.write_lead_project_log(current_lead_id, project_id, self._name)
        super(Project, self).write(vals)
        return True

    def write_lead_project_log(self, current_lead_id, project_id, model_name):
        _logger.info('project_id=%s' % project_id)
        _logger.info('current_lead_id=%s' % current_lead_id)
        self.env['crm.lead.project.project.log'].create({
            'lead_id': current_lead_id,
            'project_id': project_id,
            'model_name': model_name,
        })

    def write_from_crm(self, lead_id):
        super(Project, self).write({'lead_id': lead_id})


class CrmLeadProjectLog(models.Model):
    _name = 'crm.lead.project.project.log'
    _description = 'change log of crm.lead and project.project'

    lead_id = fields.Many2one('crm.lead', string='Opportunity', ondelete='set null')
    project_id = fields.Many2one('project.project', string='Project', ondelete='set null')
    model_name = fields.Char('model initiating the connection')
