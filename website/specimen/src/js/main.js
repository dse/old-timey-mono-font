// Copyright 2019 Google LLC

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     https://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import "./assets.js";
import fontData from "../_data/fontdata.json";
import FontFaceObserver from "fontfaceobserver";

const fontTimeOut = 5000; // In milliseconds
const fontClasses = fontData.map(f => f.selector);

// Generic: throttle
const throttle = (fn, wait) => {
	let last, queue;

	return function runFn(...args) {
		const now = Date.now();
		queue = clearTimeout(queue);

		if (!last || now - last >= wait) {
			fn.apply(null, args);
			last = now;
		} else {
			queue = setTimeout(runFn.bind(null, ...args), wait - (now - last));
		}
	};
};

// Set up FontFaceObserver
let observers = [];
for (const fd of fontData) {
	const font = new FontFaceObserver(fd.name);
	observers.push(font.load(null, fontTimeOut));
}

Promise.all(observers).then(
	() => {
		// All fonts have loaded
		document.documentElement.classList.add("fonts-loaded");
	},
	() => {
		// One or more fonts didn't load
		document.documentElement.classList.add("fonts-failed");
	}
);

// Interactive controls (sliders that tweak axes)
const interactives = document.querySelectorAll(".interactive-controls");
for (const interactive of interactives) {
	const area = interactive.querySelector(".interactive-controls-text");
	const styles = interactive.querySelector(".interactive-controls-styles");
	const sliders = interactive.querySelectorAll(
		".interactive-controls-slider"
	);
	const instances = interactive.querySelector(
		".interactive-controls-instances"
	);

	const varset = (name, value) => {
		area.style.setProperty(`--${name}`, value);
	};

	for (const slider of sliders) {
		// Apply initial axis value to text area
		varset(slider.name, slider.value);
		slider.oninput = e => {
			// Set new axis value to text area
			varset(e.target.name, e.target.value);
			// Unselect named instance dropdown
			// Optionally, see if current axes match instance and select that
			if (instances) {
				instances.selectedIndex = -1;
			}
		};
	}

	if (instances) {
		instances.onchange = e => {
			const axes = JSON.parse(
				e.target.options[e.target.selectedIndex].value
			);
			for (const axis in axes) {
				// Set new axis value on slider
				interactive.querySelector(`[name=${axis}]`).value = axes[axis];
				// Apply new axis value to text area
				varset(axis, axes[axis]);
			}
		};
	}

	if (styles) {
		styles.onchange = e => {
			area.classList.remove(...fontClasses);
			area.classList.add(e.target.value);
		};
	}

	// Alignment controls for type tester
	// Add active class to the current button (highlight it)
	const buttonContainer = interactive.querySelector(
		".interactive-controls-buttons"
	);
	const buttons = buttonContainer.querySelectorAll("button");
	for (const button of buttons) {
		button.addEventListener("click", function() {
			// Update button class
			buttonContainer.querySelector(".active").classList.remove("active");
			this.classList.add("active");
			// Apply new alignment
			area.classList.remove("align-left", "align-centre", "align-right");
			area.classList.add(this.value);
		});
	}
}

// Watch if .am-i-in-view elements are visible on screen
// and apply a class accordingly
if ("IntersectionObserver" in window) {
	// eslint-disable-next-line compat/compat
	const obs = new IntersectionObserver(els => {
		els.forEach(el => {
			el.intersectionRatio > 0
				? el.target.classList.add("in-view")
				: el.target.classList.remove("in-view");
		});
	});

	const elements = document.querySelectorAll(".am-i-in-view");
	elements.forEach(el => {
		obs.observe(el);
	});
}

// Character grid
const grid = document.querySelector(".character-grid");
const gridzoom = document.querySelector(".character-grid-zoom");
const gridtoggle = document.querySelector(".character-grid-toggle");
grid.onmousemove = throttle(e => {
	if (e.target.tagName === "LI") {
		gridzoom.innerHTML = e.target.innerHTML;
	}
}, 100);
if (gridtoggle) {
	gridtoggle.onchange = e => {
		grid.classList.remove(...fontClasses);
		grid.classList.add(e.target.value);
	};
}
