setupColorSchemeControls();
setupFontChooserControls();

function setupColorSchemeControls() {
    const form = $("#color-scheme-form");
    const html = document.documentElement;
    form.mode.forEach(radio => radio.addEventListener("change", update));
    update();
    function update(event) {
        console.log("update", form.mode.value);
        if (form.mode.value === "system") {
            html.classList.remove("color-scheme-light");
            html.classList.remove("color-scheme-dark");
            html.classList.add("color-scheme-system");
        } else if (form.mode.value === "light") {
            html.classList.remove("color-scheme-system");
            html.classList.remove("color-scheme-dark");
            html.classList.add("color-scheme-light");
        } else if (form.mode.value === "dark") {
            html.classList.remove("color-scheme-system");
            html.classList.remove("color-scheme-light");
            html.classList.add("color-scheme-dark");
        }
    }
}
function setupFontChooserControls() {
    const form = $("#font-chooser-form");
    const html = document.documentElement;
    form.font.forEach(radio => radio.addEventListener("change", update));
    update();
    function update(event) {
        console.log("update", form.font.value);
        if (form.font.value === "old-timey-mono") {
            html.classList.remove("old-timey-code");
            html.classList.remove("courier-new");
            html.classList.add("old-timey-mono");
        } else if (form.font.value === "old-timey-code") {
            html.classList.remove("old-timey-mono");
            html.classList.remove("courier-new");
            html.classList.add("old-timey-code");
        } else if (form.font.value === "courier-new") {
            html.classList.remove("old-timey-mono");
            html.classList.remove("old-timey-code");
            html.classList.add("courier-new");
        }
    }
}
function $(selectors, ctx) {
    return (ctx ?? document).querySelector(selectors);
}
function $$(selectors, ctx) {
    return [...(ctx ?? document).querySelectorAll(selectors)];
}
