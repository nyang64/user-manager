from ma import ma
from model.patient_details import PatientDetails

class PatientDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientDetails
        load_instance = True

    id = ma.auto_field(dump_only=True)
    patient_id = ma.auto_field()

