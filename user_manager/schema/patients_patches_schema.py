from ma import ma
from model.patients_patches import PatientsPatches


class PatientsPatchesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsPatches
        load_instance = True

    id = ma.auto_field(dump_only=True)
    patient_id = ma.auto_field()
    patch_lot_number = ma.auto_field()
