from werkzeug.exceptions import BadRequest, InternalServerError, Conflict
from sqlalchemy.exc import SQLAlchemyError
from model.devices import Devices
from model.device_status_types import DeviceStatusType
from model.device_statuses import DeviceStatUses
from db import db


class DeviceRepo():
    def __init__(self):
        pass

    def save_device_key(self, serial_no, encryption_key):
        import http
        try:
            exist_device = self.device_key_by_serial_number(
                serial_no=serial_no)
            print('exis', exist_device)
            if exist_device is not None:
                return exist_device,\
                    f"Device Exist with serial number {serial_no}",\
                    http.client.CONFLICT
            new_device = Devices(serial_number=serial_no,
                                 encryption_key=encryption_key)
            Devices.save_db(new_device)
            if new_device.id is None:
                raise SQLAlchemyError('Error while adding device')
            self.assign_device_status(new_device.id)
            return new_device, "Success and Device status added",\
                http.client.CREATED
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
        except (TypeError, NameError) as error:
            raise BadRequest(str(error))

    def assign_device_status(self, device_id):
        self._check_device_id_exist(device_id)
        try:
            device_status = DeviceStatUses(status_id=1,
                                           device_id=device_id)
            DeviceStatUses.save_db(device_status)
            if device_status.id is None:
                raise SQLAlchemyError('Error while assign device')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def device_key_by_serial_number(self, serial_no=None):
        if serial_no is None:
            raise BadRequest('serial_number is None')
        exist_device = db.session.query(Devices.serial_number,
                                        Devices.encryption_key).filter_by(
                                            serial_number=serial_no).first()
        if exist_device is None:
            return None
        else:
            return exist_device

    def add_device_status(self, status_name):
        try:
            self._check_status_name_exist(status_name)
            device_status = DeviceStatusType(name=status_name)
            Devices.save_db(device_status)
            return device_status
        except (TypeError, SQLAlchemyError) as e:
            raise InternalServerError(str(e))

    def _check_status_name_exist(self, status_name):
        try:
            exist_status = db.session.query(DeviceStatusType.name)\
                .filter_by(name=status_name).first()
            if bool(exist_status):
                raise Conflict('status already exist')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def _check_device_id_exist(self, device_id):
        try:
            exist_device = db.session.query(Devices.id)\
                .filter_by(id=device_id).first()
            if bool(exist_device) is False:
                raise Conflict('Device id not exist')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
