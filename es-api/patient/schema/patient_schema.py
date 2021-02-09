from user.schema.user_schema import CreateUserSchema 
from model.patient import Patient
from marshmallow import fields, validate, ValidationError

ENAME_MISSING = "emergenct_contact_name parameter is missing"
ENUMBER_MISSING = "emergenct_contact_number parameter is missing"
DOB_MISSING = "emergenct_contact_number parameter is missing"


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


class CreatePatientSchema(CreateUserSchema):
    emergency_contact_name = fields.Str(required=True,
                                        validate=must_not_blank)
    emergency_contact_number = fields.Str(required=True,
                                          validate=must_not_blank)
    date_of_birth = fields.Str(required=True,
                               validate=must_not_blank)


class UpdatePatientSchema(CreatePatientSchema):
    patient_id = fields.Int(required=True,
                            attribute="id",
                            validate=must_not_blank)


update_patient_schema = UpdatePatientSchema()
update_patients_schema = UpdatePatientSchema(many=True)
