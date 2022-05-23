from ma import ma
from model.patient_facilities import PatientFacilities

class PatientFacilitiesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientFacilities
        load_instance = True

    id = ma.auto_field(dump_only=True)
    patient_id = ma.auto_field()
    facility_id = ma.auto_field()
