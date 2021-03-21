from ma import ma
from model.patients_devices import PatientsDevices


class PatientsDevicesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsDevices
        load_instance = True

    id = ma.auto_field(dump_only=True)
    patient_id = ma.auto_field()
    device_serial_number = ma.auto_field()
