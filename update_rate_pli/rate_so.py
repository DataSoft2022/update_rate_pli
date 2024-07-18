
import frappe
from frappe.model.document import Document
from frappe import _
from erpnext.setup.utils import get_exchange_rate
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html

# @frappe.whitelist(allow_guest=True)
# def update_conversion_rate(sales_order_name, new_conversion_rate, handler=None, ignore_permission=True):
#     try:
#         # Get the Sales Order document
#         user_roles = frappe.get_roles(frappe.session.user)
        
#         # Ensure the user has permission to update Sales Orders
#         if 'submit' in user_roles:  # Assuming 'submit' is a role name that grants permission
#             so = frappe.get_doc('Sales Order', sales_order_name)
#             so.flags.ignore_validate_update_after_submit = True
#             so.flags.ignore_validate = True
#             so.flags.ignore_mandatory = True
#             # Update the conversion rate
#             so.conversion_rate = new_conversion_rate
#             print(so.conversion_rate)
#             # Update all items in the Sales Order
#             for item in so.items:
#                 item.base_rate = new_conversion_rate
              
            # print("nnnnnnnnnnnnnnnnnnnn")
            # company_currency = frappe.db.get_value(
            #         "Company", filters={"name": so.company}, fieldname=["default_currency"]
            #     )
            # print(company_currency)    
            # print(get_exchange_rate(so.currency, company_currency, args="for_buying"))
            # print("nnnnnnnnnnnnnnnnnnnn")  
#             # Save the Sales Order document
#             so.save(ignore_permissions=True)
#             frappe.db.commit()
            
#             frappe.msgprint(_("Conversion rate updated successfully"))
#         else:
#             frappe.throw(_("You are not authorized to update Sales Orders"))
    
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error in update_conversion_rate"))
#         return {'error': str(e)}


@frappe.whitelist(allow_guest=True)
def update_conversion_rate(sales_order_name, new_conversion_rate):
    so = frappe.get_doc('Sales Order', sales_order_name)
    so.flags.ignore_validate_update_after_submit = True
    so.flags.ignore_validate = True
    so.flags.ignore_mandatory = True

    # set Conversion Rate Manually From Popup
    so.db_set("conversion_rate",new_conversion_rate)
    so.db_set("base_total",flt(new_conversion_rate) * flt(so.total))
    # so.db_set("base_total",new_conversion_rate)

    # set Conversion Rate Manually From Popup Into child items
    for item in so.items:
        item.db_set("base_rate",(flt(item.rate) * flt(new_conversion_rate)))
        item.db_set("base_amount",(flt(item.amount) * flt(new_conversion_rate)))
    frappe.db.commit()