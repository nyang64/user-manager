import logging

from ma import ma
from marshmallow import ValidationError, fields, post_load
from model.patient import Patient
from model.users import Users
from model.patient_details import PatientDetails
from schema.address_schema import AddressSchema
from schema.patient_details_schema import PatientDetailsSchema
from schema.base_schema import BaseSchema, validate_number
from schema.patients_devices_schema import PatientsDevices, PatientsDevicesSchema
from schema.patients_patches_schema import PatientsPatches, PatientsPatchesSchema
from schema.user_schema import CreateUserSchema, UserSchema, UpdateUserSchema

ENAME_MISSING = "emergency_contact_name parameter is missing"
ENUMBER_MISSING = "emergency_contact_number parameter is missing"
DOB_MISSING = "emergency_contact_number parameter is missing"


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


def validate_device_serial_number(data):
    """Validate the device serial number is of 8 digit or not"""
    if not data:
        raise ValidationError("parameter missing")
    if len(data) != 8:
        DEVICE_ERROR = "device_serial_number should be of 8 digit only"
        raise ValidationError(DEVICE_ERROR)


def validate_patch_lot_number(data):
    """Validate the patch lot number which should be a 9 digit character string"""
    if not data:
        raise ValidationError("parameter missing")
    if len(data) != 9:
        patch_error = "Lot number should be of 9 digit string"
        raise ValidationError(patch_error)


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True

    id = ma.auto_field(dump_only=True)
    permanent_address = ma.Nested(AddressSchema)
    shipping_address = ma.Nested(AddressSchema)
    user_id = ma.auto_field()
    devices = ma.List(ma.Nested(PatientsDevicesSchema))
    patches = ma.List(ma.Nested(PatientsPatchesSchema))
    details = ma.Nested(PatientDetailsSchema)
    user = ma.Nested(UserSchema)

class CreatePatientSchema(CreateUserSchema):
    permanent_address = fields.Nested(AddressSchema, required=False)
    shipping_address = fields.Nested(AddressSchema, required=False)
    emergency_contact_name = fields.Str(required=True, validate=must_not_blank)
    emergency_contact_number = fields.Str(required=True, validate=validate_number)
    emergency_contact_relationship = fields.Str(required=False)
    date_of_birth = fields.Str(required=True, validate=must_not_blank)
    enrolled_date = fields.Str(required=False)
    gender = fields.Str(required=True, validate=must_not_blank)
    prescribing_provider = fields.Int(required=True, validate=must_not_blank)
    outpatient_provider = fields.Int(required=True, validate=must_not_blank)
    facility_id = fields.Int(required=True, validate=must_not_blank)
    indication = fields.Str(required=True, validate=must_not_blank)
    device_serial_number = fields.Str(required=False)
    mobile_app_user = fields.Bool(required=False)

    # Patient details. Can be grouped later
    upper_patch_setting = fields.Str(required=False)
    pa_setting_back = fields.Str(required=False)
    shoulder_strap_back = fields.Str(required=False)
    other_phone = fields.Str(required=False)
    shoulder_strap_front = fields.Str(required=False)
    pa_setting_front = fields.Str(required=False)
    starter_kit_lot_number = fields.Str(required=True)
    mobile_model = fields.Str(required=False)
    mobile_os_version = fields.Str(required=False)
    enrollment_notes = fields.Str(required=False)

    #Patches
    applied_patch_lot_number = fields.Str(required=False)
    unused_patch_lot_number = fields.Str(required=False)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        register, user = super().make_post_load_object(data)
        patient_details = {
            "patient": {
                "emergency_contact_name": data.get("emergency_contact_name"),
                "emergency_contact_number": data.get("emergency_contact_number"),
                "emergency_contact_relationship": data.get("emergency_contact_relationship"),
                "date_of_birth": data.get("date_of_birth"),
                "enrolled_date":data.get("enrolled_date"),
                "gender": data.get("gender"),
                "indication": data.get("indication"),
                "mobile_app_user": data.get("mobile_app_user"),
                "permanent_address": data.get("permanent_address"),
                "shipping_address": data.get("shipping_address")
            },
            "providers": {
                "prescribing_provider_id": data.get("prescribing_provider"),
                "outpatient_provider_id": data.get("outpatient_provider"),
            },
            "facility": {"facility_id": data.get("facility_id")},
            "device": {"serial_number": data.get("device_serial_number")},
            "patches": {
                "applied_patch_lot_number": data.get("applied_patch_lot_number"),
                "unused_patch_lot_number": data.get("unused_patch_lot_number")
            },
            "details": {
                "upper_patch_setting": data.get("upper_patch_setting"),
                "pa_setting_back": data.get("pa_setting_back"),
                "shoulder_strap_back": data.get("shoulder_strap_back"),
                "other_phone": data.get("other_phone"),
                "shoulder_strap_front": data.get("shoulder_strap_front"),
                "pa_setting_front": data.get("pa_setting_front"),
                "starter_kit_lot_number": data.get("starter_kit_lot_number"),
                "mobile_model": data.get("mobile_model"),
                "mobile_os_version": data.get("mobile_os_version"),
                "enrollment_notes": data.get("enrollment_notes")
            }
        }

        return register, user, patient_details


create_patient_schema = CreatePatientSchema()
patients_schema = CreatePatientSchema(many=True)


# Creating a new schema to return objects instead of returning tuples. Will create a story to standardize the
# schema creation for post clinical trials
class UpdatePatientSchema(BaseSchema):
    permanent_address = fields.Nested(AddressSchema, required=False)
    shipping_address = fields.Nested(AddressSchema, required=False)
    emergency_contact_name = fields.Str(required=True, validate=must_not_blank)
    emergency_contact_number = fields.Str(required=True, validate=validate_number)
    emergency_contact_relationship = fields.Str(required=False)
    date_of_birth = fields.Str(required=True, validate=must_not_blank)
    enrolled_date = fields.Str(required=False)
    gender = fields.Str(required=True, validate=must_not_blank)
    prescribing_provider = fields.Int(required=True, validate=must_not_blank)
    outpatient_provider = fields.Int(required=True, validate=must_not_blank)
    facility_id = fields.Int(required=True, validate=must_not_blank)
    indication = fields.Str(required=True, validate=must_not_blank)
    device_serial_number = fields.Str(required=False)
    mobile_app_user = fields.Bool(required=False)
    email = fields.Str(required=False)
    first_name = fields.Str(required=True, validate=must_not_blank)
    last_name = fields.Str(required=True, validate=must_not_blank)
    phone_number = fields.Str(required=True, validate=must_not_blank)
    external_user_id = fields.Str(required=False)

    # Patient details. Can be grouped later
    upper_patch_setting = fields.Str(required=False)
    pa_setting_back = fields.Str(required=False)
    shoulder_strap_back = fields.Str(required=False)
    other_phone = fields.Str(required=False)
    shoulder_strap_front = fields.Str(required=False)
    pa_setting_front = fields.Str(required=False)
    starter_kit_lot_number = fields.Str(required=True)
    mobile_model = fields.Str(required=False)
    mobile_os_version = fields.Str(required=False)
    enrollment_notes = fields.Str(required=False)

    # Patches
    applied_patch_lot_number = fields.Str(required=False)
    unused_patch_lot_number = fields.Str(required=False)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        user = Users(first_name=data.get("first_name"),
                     last_name=data.get("last_name"),
                     phone_number=data.get("phone_number"),
                     external_user_id=data.get("external_user_id"))

        email = data.get("email")
        patient = Patient(emergency_contact_name=data.get("emergency_contact_name"),
                          emergency_contact_number=data.get("emergency_contact_number"),
                          emergency_contact_relationship=data.get("emergency_contact_relationship"),
                          date_of_birth=data.get("date_of_birth"),
                          enrolled_date=data.get("enrolled_date"),
                          gender=data.get("gender"),
                          indication=data.get("indication"),
                          mobile_app_user=data.get("mobile_app_user"),
                          permanent_address=data.get("permanent_address"),
                          shipping_address=data.get("shipping_address"))

        patient_details = {
            "providers": {
                "prescribing_provider_id": data.get("prescribing_provider"),
                "outpatient_provider_id": data.get("outpatient_provider"),
            },
            "facility": {"facility_id": data.get("facility_id")},
            "device": {"serial_number": data.get("device_serial_number")},
            "details": {
                "upper_patch_setting": data.get("upper_patch_setting"),
                "pa_setting_back": data.get("pa_setting_back"),
                "shoulder_strap_back": data.get("shoulder_strap_back"),
                "other_phone": data.get("other_phone"),
                "shoulder_strap_front": data.get("shoulder_strap_front"),
                "pa_setting_front": data.get("pa_setting_front"),
                "starter_kit_lot_number": data.get("starter_kit_lot_number"),
                "mobile_model": data.get("mobile_model"),
                "mobile_os_version": data.get("mobile_os_version"),
                "enrollment_notes": data.get("enrollment_notes")
            },
            "patches": {
                "applied_patch_lot_number": data.get("applied_patch_lot_number"),
                "unused_patch_lot_number": data.get("unused_patch_lot_number")
            }
        }
        return user, email, patient, patient_details

# Both create and update patient schemas are the same for now
update_patient_schema = UpdatePatientSchema()
update_patients_schema = UpdatePatientSchema(many=True)


class AssignDeviceSchema(BaseSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsDevices
        load_instance = True
        include_fk = True

    device_serial_number = fields.Str(
        required=True, validate=validate_device_serial_number
    )


assign_device_schema = AssignDeviceSchema()


class AssignPatchesSchema(BaseSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsPatches
        load_instance = True
        include_fk = True

    patch_lot_number = fields.Str(
        required=True, validate=validate_patch_lot_number
    )


assign_patches_schema = AssignPatchesSchema()


class PatientDetailSchema(BaseSchema):
    patient_id = fields.Int(attribute="id", dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    external_user_id = fields.Str(dump_only=True)
    mobile = fields.Str(attribute="phone_number", dump_only=True)
    date_of_birth = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    enrolled_on = fields.Str(attribute="enrolled_date", dump_only=True)
    unenrolled_on = fields.Str(attribute="unenrolled_at", dump_only=True)
    emergency_contact_name = fields.Str(dump_only=True)
    emergency_contact_number = fields.Str(dump_only=True)
    status = fields.Str(attribute="name", dump_only=True)
    indication = fields.Str(attribute="indication", dump_only=True)
    street_address_1 = fields.Str(dump_only=True)
    street_address_2 = fields.Str(dump_only=True)
    city = fields.Str(dump_only=True)
    state = fields.Str(dump_only=True)
    country = fields.Str(dump_only=True)
    postal_code = fields.Str(dump_only=True)


patient_detail_schema = PatientDetailSchema()


class FilterPatientSchema(BaseSchema):
    page_number = fields.Int(required=True, load_only=True)
    record_per_page = fields.Int(load_only=True)
    first_name = fields.Str(load_only=True)
    last_name = fields.Str(load_only=True)
    date_of_birth = fields.Str(load_only=True)
    report_id = fields.Int(load_only=True)
    external_user_id = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        date_of_birth = data.get("date_of_birth", None)
        external_user_id = data.get("external_user_id", None)
        try:
            page_number = int(data.get("page_number", 0))
            record_per_page = int(data.get("record_per_page", 10))
            report_id = int(data.get("report_id", 0))
        except ValueError as e:
            logging.error(e)
            page_number = 0
            record_per_page = 10
            report_id = 0
        filter_input = (
            page_number,
            record_per_page,
            first_name,
            last_name,
            date_of_birth,
            report_id,
            external_user_id
        )
        return filter_input


filter_patient_schema = FilterPatientSchema()


class PatientListSchema(BaseSchema):
    page_number = fields.Int(required=True, load_only=True)
    record_per_page = fields.Int(load_only=True)
    name = fields.Str(load_only=True)
    external_id = fields.Str(load_only=True)
    site_id = fields.Int(load_only=True)
    provider_id = fields.Int(load_only=True)
    status = fields.Str(load_only=True)
    id = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        try:
            name = data.get("name", None)
            page_number = int(data.get("page_number", 0))
            record_per_page = int(data.get("record_per_page", 10))
            id = data.get("id", None)
            external_id = data.get("external_id", None)
            site_id = int(data.get("site_id", 0))
            provider_id = int(data.get("provider_id", 0))
            status = data.get("status", None)
        except ValueError as e:
            logging.error(e)
            page_number = 0
            record_per_page = 10
            external_id = ""
            name = ""
        filter_input = (
            page_number,
            record_per_page,
            name,
            external_id,
            site_id,
            provider_id,
            status,
            id
        )
        return filter_input


patient_list_schema = PatientListSchema()


class PatientIdSchema(BaseSchema):
    patientID = fields.Int(required=True, validate=must_not_blank, load_only=True)


patient_id_schema = PatientIdSchema()


class DeactivatePatientSchema(BaseSchema):
    patient_id = fields.Int(required=True, load_only=True)
    deactivation_reason = fields.List(fields.String, load_only=True)
    notes = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        try:
            patient_id = int(data.get("patient_id", None))
            deactivation_reason = data.get("deactivation_reason", "")
            notes = data.get("notes", "")
        except ValueError as e:
            logging.error(e)

        filter_input = (patient_id, deactivation_reason, notes)
        return filter_input


deactivate_patient_schema = DeactivatePatientSchema()

