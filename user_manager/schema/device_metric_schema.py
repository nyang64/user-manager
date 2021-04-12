from model.device_metric import DeviceMetric
from ma import ma


class DeviceMetricSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceMetric
        load_instance = True

    id = ma.auto_field(dump_only=True)
