/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { DiscountButton } from "@pos_discount/overrides/components/discount_button/discount_button";


patch(DiscountButton.prototype, {

    async apply_discount(pc) {
        const order = this.pos.get_order();
        const lines = order.get_orderlines();
        if (this.pos.config.is_discount_fixed){
            const product = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
            if (product === undefined && this.pos.config.apply_on == 'order') {
                await this.popup.add(ErrorPopup, {
                    title: _t("No discount product found"),
                    body: _t(
                        "The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."
                    ),
                });
                return;
            }

            // Remove existing discounts
            lines
                .filter((line) => line.get_product() === product)
                .forEach((line) => order._unlinkOrderline(line));

            // Add one discount line per tax group
            const linesByTax = order.get_orderlines_grouped_by_tax_ids();
            for (const [tax_ids, lines] of Object.entries(linesByTax)) {
                // Note that tax_ids_array is an Array of tax_ids that apply to these lines
                // That is, the use case of products with more than one tax is supported.
                const tax_ids_array = tax_ids
                    .split(",")
                    .filter((id) => id !== "")
                    .map((id) => Number(id));

                const baseToDiscount = order.calculate_base_amount(
                    tax_ids_array,
                    lines.filter((ll) => ll.isGlobalDiscountApplicable())
                );
                pc = (pc / baseToDiscount) * 100
            }
        }
        if (this.pos.config.discount_limit && pc > this.pos.config.discount_limit_pc){
            pc = Math.max(0, Math.min(100, parseFloat(this.pos.config.discount_limit_pc)));
            this.env.services.pos_notification.add(
                _t('Maximum discount(%) allowed: %s', this.pos.config.discount_limit_pc.toString()), 3000);
        }
        if (this.pos.config.apply_on == 'lines'){
            for (const line of lines){
                line.set_discount(pc);
            }
        } else{
            return await super.apply_discount(pc);
        }
    }

});

ProductScreen.addControlButton({
    component: DiscountButton,
    condition: function () {
        const { module_pos_discount, discount_product_id, apply_on } = this.pos.config;
        return module_pos_discount && (discount_product_id || apply_on == 'lines');
    },
    position: ['replace', 'DiscountButton']
});
