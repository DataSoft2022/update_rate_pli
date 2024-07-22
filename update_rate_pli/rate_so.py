
import frappe
from frappe.model.document import Document
from frappe import _
from erpnext.setup.utils import get_exchange_rate
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html
from frappe.utils import money_in_words


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
    so.db_set("base_total_taxes_and_charges",flt(new_conversion_rate) * flt(so.total_taxes_and_charges))
    so.db_set("base_grand_total",flt(new_conversion_rate) * flt(so.grand_total))
    so.db_set("base_rounded_total",flt(new_conversion_rate) * flt(so.rounded_total))
    print(so.company_currency)
    print(so.base_rounded_total)
    so.db_set("base_in_words",money_in_words(so.base_rounded_total,so.company_currency))
    
    # set Conversion Rate Manually From Popup Into child items
    for item in so.items:
        item.db_set("base_rate",(flt(item.rate) * flt(new_conversion_rate)))
        item.db_set("base_amount",(flt(item.amount) * flt(new_conversion_rate)))
    for tax in so.taxes:
        tax.db_set("base_tax_amount",flt(tax.tax_amount)*flt(new_conversion_rate))    
        tax.db_set("base_total",flt(tax.total)*flt(new_conversion_rate))


    frappe.db.commit()
