from user.schema.user_schema import CreateUserSchema
from model.schema.base_schema import validate_number, BaseSchema
from marshmallow import fields, ValidationError, post_load

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
                                          validate=validate_number)
    date_of_birth = fields.Str(required=True,
                               validate=must_not_blank)

    @post_load
    def make_post_dump_object(self, data, **kwargs):
        print(data)
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_number = data.get('emergency_contact_number')
        date_of_birth = data.get('date_of_birth')
        register = (email, password)
        user = (first_name, last_name, phone_number)
        patient = (emergency_contact_name,
                   emergency_contact_number, date_of_birth)
        return register, user, patient


create_patient_schema = CreatePatientSchema()
patients_schema = CreatePatientSchema(many=True)


class UpdatePatientSchema(BaseSchema):
    emergency_contact_name = fields.Str(required=True,
                                        validate=must_not_blank)
    emergency_contact_number = fields.Str(required=True,
                                          validate=validate_number)
    date_of_birth = fields.Str(required=True,
                               validate=must_not_blank)
    
    @post_load
    def make_post_dump_object(self, data, **kwargs):
        print(data)
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_number = data.get('emergency_contact_number')
        date_of_birth = data.get('date_of_birth')
        patient = (emergency_contact_name,
                   emergency_contact_number, date_of_birth)
        return patient


update_patient_schema = UpdatePatientSchema()
update_patients_schema = UpdatePatientSchema(many=True)


class AssignDeviceSchema(BaseSchema):
    patient_id = fields.Int(required=True,
                            validate=must_not_blank)
    device_id = fields.Int(required=True,
                           validate=must_not_blank)

    @post_load
    def post_load_object(self, data, **kwargs):
        patient_id = data.get('patient_id')
        device_id = data.get('device_id')
        return patient_id, device_id


assign_device_schema = AssignDeviceSchema()
