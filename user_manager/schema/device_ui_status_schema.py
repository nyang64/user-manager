from model.device_ui_status import DeviceUiStatus
from ma import ma


class DeviceUiStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceUiStatus
        load_instance = True

    id = ma.auto_field(dump_only=True)
    status_id = ma.auto_field()
