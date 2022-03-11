import logging

from marshmallow import ValidationError, fields, post_load
from schema.address_schema import AddressSchema
from schema.base_schema import BaseSchema
from services.material_request_services import MaterialRequestObj
from utils.common import format_phone_number


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class AddMaterialSchema(BaseSchema):
    address = fields.Nested(AddressSchema, required=False)
    requestor_first_name = fields.Str(required=True, validate=must_not_blank)
    requestor_last_name = fields.Str(required=True, validate=must_not_blank)
    date_requested = fields.Str(required=True)
    date_needed = fields.Str(required=True, validate=must_not_blank)
    protocol_number  = fields.Str(required=True)
    patient_id = fields.Int(required=False)
    site_id = fields.Int(required=False)
    site_name = fields.Str(required=True)
    recipient_name = fields.Str(required=True)
    recipient_phone = fields.Str(required=True, validate=must_not_blank)
    recipient_email = fields.Str(required=True, validate=must_not_blank)
    special_instructions = fields.Str(required=False)
    requested_product = fields.Dict(keys=fields.Str(), values=fields.Int())
    requested_return_product = fields.Dict(keys=fields.Str(), values=fields.Int())
    complaint_request = fields.Bool(required=False)

    @post_load
    def load_data(self, data, **kwargs):
        req_obj = MaterialRequestObj()
        req_obj.needed_by_date = data.get("date_needed")
        req_obj.date_requested =data.get("date_requested")
        req_obj.loggedin_user = data.get("requestor_first_name") + " " + data.get("requestor_last_name")
        req_obj.address = data.get("address").street_address_1
        if data.get("address").street_address_2 is not None and \
                len(data.get("address").street_address_2) > 0:
            req_obj.address = req_obj.address + " " + data.get("address").street_address_2
        req_obj.city = data.get("address").city
        req_obj.state = data.get("address").state
        req_obj.country = data.get("address").country
        req_obj.zip = data.get("address").postal_code
        req_obj.phone = format_phone_number(data.get("recipient_phone"))
        req_obj.email = data.get("recipient_email")

        # requested new products
        req_obj.patch_kit_qty = data.get("requested_product").get("patch_unit")
        req_obj.mdu_qty = data.get("requested_product").get("mdu")
        req_obj.starter_kit_qty = data.get("requested_product").get("starter_kit")
        req_obj.skin_prep_kit_qty = data.get("requested_product").get("skin_prep_kit")
        req_obj.removal_kit_qty = data.get("requested_product").get("removal_kit")
        req_obj.placement_accessory_qty = data.get("requested_product").get("placement_accessory")
        req_obj.ht_qty = data.get("requested_product").get("hair_trimmer")
        req_obj.ifu_qty = data.get("requested_product").get("ifu")
        req_obj.adhesive_laminate_qty = data.get("requested_product").get("adhesive_laminate")

        req_obj.mdu_return_qty = data.get("requested_return_product").get("mdu_return")
        req_obj.patch_return_qty = data.get("requested_return_product").get("patch_unit_return")
        req_obj.placement_accessory_return_qty = data.get("requested_return_product").get("placement_accessory_return")
        req_obj.return_label_qty = data.get("requested_return_product").get("return_label")

        req_obj.special_instructions = data.get("special_instructions")

        if data.get("complaint_request") is True:
            req_obj.complaint_request = "Yes"
        else:
            req_obj.complaint_request = "No"

        req_obj.site_id = data.get("site_id")
        req_obj.patient_id = data.get("patient_id")

        if data.get("special_instructions") is None or\
                len(data.get("special_instructions")) == 0:
            req_obj.special_instructions = "N/A"
        else:
            req_obj.special_instructions = data.get("special_instructions")

        if data.get("site_name") is None or len(data.get("site_name")) == 0:
            req_obj.site_name = "N/A"
        else:
            req_obj.site_name = data.get("site_name")
        req_obj.recipient_name = data.get("recipient_name")

        return req_obj



class MaterialListSchema(BaseSchema):
    page_number = fields.Int(required=True, load_only=True)
    record_per_page = fields.Int(load_only=True)
    request_number = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        default_page_number = 0
        default_record_per_page = 10

        try:
            request_number = data.get("request_number", None)
            page_number = int(data.get("page_number", default_page_number))
            record_per_page = int(data.get("record_per_page", default_record_per_page))
        except ValueError as e:
            logging.error(e)
            page_number = default_page_number
            record_per_page = default_record_per_page
        filter_input = (page_number, record_per_page, request_number)
        return filter_input


material_list_schema = MaterialListSchema()
add_materials_schema = AddMaterialSchema()
