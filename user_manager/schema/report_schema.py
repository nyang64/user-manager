from schema.base_schema import BaseSchema
from marshmallow import fields, ValidationError


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class PatientReportSchema(BaseSchema):
    id = fields.Int(dump_only=True, data_key='report_id')
    created_at = fields.Str(dump_only=True)
    clinician_verified_at = fields.Str(data_key="uploaded_ts", dump_only=True)


patient_reports_schema = PatientReportSchema(many=True)


class ReportIdSchema(BaseSchema):
    reportId = fields.Int(required=True,
                          validate=must_not_blank,
                          load_only=True)


report_id_schema = ReportIdSchema()
