/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { DomainSelectorDialog } from "@web/core/domain_selector_dialog/domain_selector_dialog";
import { getDefaultDomain } from "@web/core/domain_selector/utils";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

patch(FormController.prototype, {

	setup() {
		super.setup(...arguments);
		this.action = useService("action");
	},

	async beforeExecuteActionButton(clickParams) {

		let div = document.getElementsByName("model_name")[0];
		let resModel = div.querySelector("span").innerHTML;

		if (clickParams.context === "{'domain_dialogue':'1'}" && resModel) {
			var domain = "[]";
			var current_model = this.model.root.resModel
			var resId = this.model.root.resId

			this.dialogService.add(DomainSelectorDialog, {
				resModel: resModel,
				defaultConnector: "|",
				domain,
				onConfirm: (domain) => this.splitAndAddDomain(domain,resModel),
				disableConfirmButton: (domain) => domain === `[]`,
				title: _t("Add Custom Filter"),
				confirmButtonText: _t("Add"),
				discardButtonText: _t("Cancel"),
			});
		}
		return super.beforeExecuteActionButton(...arguments);
	},

	splitAndAddDomain(domain,resModel) {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "Global Search",
			res_model: "global.search.wizard",
			view_mode: "form",
			views: [
				[false, "form"]
			],
			target: "new",
			context: {
				default_domain: domain,
				default_model_name: resModel,
			}
		});
	}

});