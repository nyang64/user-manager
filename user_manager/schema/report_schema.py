from schema.base_schema import BaseSchema
from marshmallow import fields, ValidationError


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class PatientReportSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.Str(dump_only=True)
    uploaded_ts = fields.Str(attributes="updated_at", dump_only=True)


patient_reports_schema = PatientReportSchema(many=True)


class ReportIdSchema(BaseSchema):
    reportId = fields.Int(required=True,
                          validate=must_not_blank,
                          load_only=True)


report_id_schema = ReportIdSchema()
