/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import {parseFloat as oParseFloat} from "@web/views/fields/parsers";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {

    async updateSelectedOrderline({buffer, key}) {
        const val = buffer === null ? "remove" : buffer;
        if (val != "remove"){
            if (this.pos.numpadMode == "discount"){
                const discount_val = typeof val === "number" ? val : isNaN(parseFloat(val)) ? 0 : oParseFloat("" + val);
                if (this.pos.config.discount_line_limit && discount_val > this.pos.config.discount_line_limit_pc) {
                    return this.notification.add(_t(
                        "Maximum discount you can set is %s.",
                        this.env.utils.formatProductQty(this.pos.config.discount_line_limit_pc)
                    ), 3000);
                }
            }
        }
        return super.updateSelectedOrderline({buffer, key})
    },

});
