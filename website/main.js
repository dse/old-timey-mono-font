function initCodeVariantCheckbox() {
    var checkbox = document.getElementById("code-checkbox");
    var element = (document.getElementById("whole-char-list") ||
                   document.getElementById("whole-char-grid"));
    if (!element) {
        return;
    }
    checkbox.addEventListener("change", update);
    var checked = JSON.parse(localStorage.getItem("reproTypewrCodeCheckboxChecked"));
    console.log(checked);
    checkbox.checked = checked;
    function update() {
        if (checkbox.checked) {
            element.classList.add("code");
            localStorage.setItem("reproTypewrCodeCheckboxChecked", "true");
            console.log("true");
        } else {
            element.classList.remove("code");
            localStorage.setItem("reproTypewrCodeCheckboxChecked", "false");
            console.log("false");
        }
    }
}

if (document.readyState === 'complete') {
    initCodeVariantCheckbox();
} else {
    window.addEventListener('load', initCodeVariantCheckbox);
}
