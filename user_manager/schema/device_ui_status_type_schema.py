from model.device_ui_status_type import DeviceUiStatusType
from ma import ma


class DeviceUiStatusTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceUiStatusType
        load_instance = True

    id = ma.auto_field(dump_only=True)
