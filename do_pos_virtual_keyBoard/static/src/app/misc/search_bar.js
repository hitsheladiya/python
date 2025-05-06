/** @odoo-module **/

import { SearchBar } from "@point_of_sale/app/screens/ticket_screen/search_bar/search_bar";
import { OnscreenKeyboardSimple } from "@do_pos_virtual_keyBoard/app/screens/productscreen/onscreenkeyboard";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(SearchBar.prototype, {
	/**
	 * Needs to be set to true to show the loyalty points in the partner list.
	 * @override
	 */
	
	setup() {
		super.setup(...arguments);
		this.pos = usePos();
	},

	_onClickProductSearch(event) {
		if(this.pos.config.iface_vkeyboard){
			OnscreenKeyboardSimple.prototype.connect(event.currentTarget);
		}
	},
});