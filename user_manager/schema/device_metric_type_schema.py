from model.device_metric_type import DeviceMetricType
from ma import ma


class DeviceMetricTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceMetricType
        load_instance = True

    id = ma.auto_field(dump_only=True)
