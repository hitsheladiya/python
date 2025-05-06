/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dropdown } from '@web/core/dropdown/dropdown';
import { DropdownItem } from '@web/core/dropdown/dropdown_item';

class GlobalSearchIcon extends Component {
	
	setup() {
		super.setup(...arguments);
		this.action = useService("action");
	}
	
	_openGlobalWizard() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "Global Search",
			res_model: "global.search.wizard",
			view_mode: "form",
			views: [
				[false, "form"]
			],
			target: "new",
		});
	}
}

GlobalSearchIcon.template = "global_search_icon";
GlobalSearchIcon.components = { Dropdown, DropdownItem };
export const systrayItem = { Component: GlobalSearchIcon, };
registry.category("systray").add("GlobalSearchIcon", systrayItem, { sequence: 1 });