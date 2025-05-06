/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Chrome } from "@point_of_sale/app/pos_app";
import { useOwnDebugContext } from "@web/core/debug/debug_context";
import { user } from "@web/core/user";

export class OnscreenKeyboardSimple extends Component {
	static template = "do_pos_virtual_keyBoard.OnscreenKeyboardSimple";

	setup() {
		super.setup(...arguments);
	}

	keyboardClose(event) {
		this.hide();
	}

	keyboardClick(event) {
		var self = this;
		var $this = event.target;
		var character = $this.innerHTML; // If it's a lowercase letter, nothing happens to this variable

		if ($this.className.includes("left-shift") || $this.className.includes("right-shift")) {
			self.toggleShift();
			return false;
		}

		if ($this.className.includes('capslock')) {
			self.toggleCapsLock();
			return false;
		}

		if ($this.className.includes('delete')) {
			self.deleteCharacter();
			return false;
		}

		if ($this.className.includes('numlock')) {
			self.toggleNumLock();
			return false;
		}

		// Special characters
		// if ($this.className.includes('symbol')) character = $('span:visible', $this).html();
		if ($this.className.includes('symbol')) character = $this.querySelector(".off").innerText;
		if ($this.className.includes('space')) character = ' ';
		if ($this.className.includes('tab')) character = "\t";
		if ($this.className.includes('return')) character = "\n";

		// Uppercase letter
		if ($this.className.includes('return')) character = character.toUpperCase();

		// Remove shift once a key is clicked.
		self.removeShift();

		self.writeCharacter($this,character);
	}
	connect(target) {
		var self = this;
		this.$target = target;
		self.show();
	}
	generateEvent(type, key) {
		var event = document.createEvent("KeyboardEvent");
		var initMethod = event.initKeyboardEvent ? 'initKeyboardEvent' : 'initKeyEvent';
		event[initMethod](type,
			true, //bubbles
			true, //cancelable
			window, //viewArg
			false, //ctrl
			false, //alt
			false, //shift
			false, //meta
			((typeof key.code === 'undefined') ? key.char.charCodeAt(0) : key.code),
			((typeof key.char === 'undefined') ? String.fromCharCode(key.code) : key.char)
		);
		return event;
	}

	// Write a character to the input zone
	writeCharacter($this,character) {
		var inputs = document.querySelectorAll('input');
		var input = inputs[inputs.length-1]

		function generateKeyboardEvent(type, character) {
			// Create a KeyboardEvent with keyCode and other properties
			var event = new KeyboardEvent(type, {
				bubbles: true,
				cancelable: true,
				key: character,  // Simulate the character key
				code: character.charCodeAt(0), // Set the charCode (or keyCode) of the character
				charCode: character.charCodeAt(0),  // Equivalent to keyCode for character keys
			});
			return event;
		}

		// Simulate 'keypress' event
		input.dispatchEvent(generateKeyboardEvent('keypress', character ));

		// If the character is not a newline, append it to the input value
		if (character !== '\n') {
			input.value += character;
		}

		// Simulate 'keyup' event
		input.dispatchEvent(generateKeyboardEvent('keyup', character ));

		// Simulate 'input' event
		input.dispatchEvent(generateKeyboardEvent('input', character ));

	}

	// Removes the last character from the input zone.
	async deleteCharacter() {
		var inputs = document.querySelectorAll('input');
		var input = inputs[inputs.length-1]

		// Simulate the 'keypress' event
		input.dispatchEvent(this.generateEvent('keypress', { code: 8 })); // Key code 8 is 'Backspace'

		// Remove the last character from the input value
		input.value = input.value.slice(0, -1);

		// Simulate the 'keyup' event
		input.dispatchEvent(this.generateEvent('keyup', { code: 8 }));

		// Simulate the 'input' event
		input.dispatchEvent(this.generateEvent('input', { char: input.value }));

	}

	show() {
		var elements = document.querySelectorAll('.keyboard_frame');
		elements.forEach(function(element) {
			element.style.height = '235px';
		});
	}

	// Makes the keyboard hide by sliding to the bottom of the screen.
	hide() {
		var elements = document.querySelectorAll('.keyboard_frame');
		elements.forEach(function(element) {
			element.style.height = '0';
		});
		this.reset();
	}
	toggleShift() {
		document.querySelectorAll('.letter').forEach(el => el.classList.toggle('uppercase'));
		var elements = document.querySelectorAll('.symbol span');
		elements.forEach(function(element) {
			if (element.classList.contains('off')) {
				element.classList.remove('off');
				element.classList.add('on');
			} else if (element.classList.contains('on')) {
				element.classList.remove('on');
				element.classList.add('off');
			}
		});
		this.shift = (this.shift === true) ? false : true;
		this.capslock = false;
	}

	//what happens when capslock is pressed : toggle case, set capslock
	toggleCapsLock() {
		document.querySelectorAll('.letter').forEach(el => el.classList.toggle('uppercase'));
		this.capslock = true;
	}

	//What happens when numlock is pressed : toggle symbols and numlock label
	toggleNumLock() {
		var elements = document.querySelectorAll('.symbol span');
		elements.forEach(function(element) {
			if (element.classList.contains('off')) {
				element.classList.remove('off');
				element.classList.add('on');
			} else if (element.classList.contains('on')) {
				element.classList.remove('on');
				element.classList.add('off');
			}
		});
		var elements = document.querySelectorAll('.numlock span');
		elements.forEach(function(element) {
			if (element.classList.contains('off')) {
				element.classList.remove('off');
				element.classList.add('on');
			} else if (element.classList.contains('on')) {
				element.classList.remove('on');
				element.classList.add('off');
			}
		});
		this.numlock = (this.numlock === true) ? false : true;
	}

	//After a key is pressed, shift is disabled.
	removeShift() {
		if (this.shift === true) {
			var elements = document.querySelectorAll('.symbol span');
			elements.forEach(function(element) {
				if (element.classList.contains('off')) {
					element.classList.remove('off');
					element.classList.add('on');
				} else if (element.classList.contains('on')) {
					element.classList.remove('on');
					element.classList.add('off');
				}
			});
			if (this.capslock === false) document.querySelectorAll('.letter').forEach(el => el.classList.toggle('uppercase'));
			this.shift = false;
		}
	}

	// Resets the keyboard to its original state; capslock: false, shift: false, numlock: false
	reset() {
		if (this.shift) {
			this.toggleShift();
		}
		if (this.capslock) {
			this.toggleCapsLock();
		}
		if (this.numlock) {
			this.toggleNumLock();
		}
	}

	get CurrentLang() {
		return user.lang
	}
}

Chrome.components = {
	...Chrome.components,
	OnscreenKeyboardSimple,
};