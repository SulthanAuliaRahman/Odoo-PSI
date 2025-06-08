/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { _t } from "@web/core/l10n/translation";
import { RestrictPopup } from "./restrict_popup";

patch(PosStore.prototype, {
    async addProductToCurrentOrder(product, options = {}) {
        // Cek apakah produk dibatasi umur
        if (product.is_age_restrict === true) {
            const minAge = product.min_age_required || 18; // default ke 18 jika undefined/null
            const { confirmed } = await this.popup.add(RestrictPopup, {
                title: _t("Pembatasan Umur!"),
                body: _t(
                    `Perhatian! Produk ini memiliki batasan umur minimal ${minAge} tahun untuk pembelian. Pastikan pembeli memenuhi syarat umur.`
                ),
            });

            if (confirmed) {
                super.addProductToCurrentOrder(product, options);
            }
        } else {
            super.addProductToCurrentOrder(product, options);
        }
    },
});
