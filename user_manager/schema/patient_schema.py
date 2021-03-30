from schema.user_schema import CreateUserSchema, UserSchema
from schema.base_schema import validate_number, BaseSchema
from model.patients_devices import PatientsDevices
from model.patient import Patient
from marshmallow import fields, ValidationError, post_load
from ma import ma
import logging


ENAME_MISSING = "emergency_contact_name parameter is missing"
ENUMBER_MISSING = "emergency_contact_number parameter is missing"
DOB_MISSING = "emergency_contact_number parameter is missing"


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


def validate_device_serial_number(data):
    '''Validate the device serial number is of 8 digit or not'''
    if not data:
        raise ValidationError('parameter missing')
    if len(data) != 8:
        DEVICE_ERROR = 'device_serial_number should be of 8 digit only'
        raise ValidationError(DEVICE_ERROR)


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True

    id = ma.auto_field(dump_only=True)
    provider_id = ma.auto_field()
    user_id = ma.auto_field()
    user = ma.Nested(UserSchema)


class CreatePatientSchema(CreateUserSchema):
    emergency_contact_name = fields.Str(required=True, validate=must_not_blank)
    emergency_contact_number = fields.Str(required=True,
                                          validate=validate_number)
    date_of_birth = fields.Str(required=True, validate=must_not_blank)
    gender = fields.Str(required=True, validate=must_not_blank)
    provider_id = fields.Int(required=True, validate=must_not_blank)
    prescribing_provider = fields.Int(required=True, validate=must_not_blank)
    outpatient_provider = fields.Int(required=True, validate=must_not_blank)
    indication = fields.Str(required=True, validate=must_not_blank)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        register, user = super().make_post_load_object(data)
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_number = data.get('emergency_contact_number')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        provider_id = data.get('provider_id')
        outpatient_provider = data.get('outpatient_provider')
        prescribing_provider = data.get('prescribing_provider')
        indication = data.get('indication')
        patient = (emergency_contact_name, emergency_contact_number,
                   date_of_birth, gender, provider_id, indication)
        # 1st is oupatient 2nd is prescribing
        provider = (outpatient_provider, prescribing_provider)
        return register, user, patient, provider


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
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_number = data.get('emergency_contact_number')
        date_of_birth = data.get('date_of_birth')
        patient = (emergency_contact_name,
                   emergency_contact_number, date_of_birth)
        return patient


update_patient_schema = UpdatePatientSchema()
update_patients_schema = UpdatePatientSchema(many=True)


class AssignDeviceSchema(BaseSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsDevices
        load_instance = True
        include_fk = True

    device_serial_number = fields.Str(required=True,
                                      validate=validate_device_serial_number)


assign_device_schema = AssignDeviceSchema()


class PatientDetailSchema(BaseSchema):
    patient_id = fields.Int(attribute="id", dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    mobile = fields.Str(attribute='phone_number', dump_only=True)
    date_of_birth = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    enrolled_on = fields.Str(dump_only=True)
    emergency_contact_name = fields.Str(dump_only=True)
    emergency_contact_number = fields.Str(dump_only=True)
    # address = fields.Str(attribute='full_address', dump_only=True)
    status = fields.Str(attribute='name', dump_only=True)
    indication = fields.Str(attribute='indication', dump_only=True)


patient_detail_schema = PatientDetailSchema()


class FilterPatientSchema(BaseSchema):
    page_number = fields.Int(required=True,
                             load_only=True)
    record_per_page = fields.Int(load_only=True)
    first_name = fields.Str(load_only=True)
    last_name = fields.Str(load_only=True)
    date_of_birth = fields.Str(load_only=True)
    report_id = fields.Int(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        date_of_birth = data.get('date_of_birth', None)
        try:
            page_number = int(data.get('page_number', 0))
            record_per_page = int(data.get('record_per_page', 10))
            report_id = int(data.get('report_id', 0))
        except ValueError as e:
            logging.error(e)
            page_number = 0
            record_per_page = 10
            report_id = 0
        filter_input = (page_number, record_per_page, first_name,
                        last_name, date_of_birth, report_id)
        return filter_input


filter_patient_schema = FilterPatientSchema()


class PatientIdSchema(BaseSchema):
    patientID = fields.Int(required=True,
                           validate=must_not_blank,
                           load_only=True)


patient_id_schema = PatientIdSchema()
