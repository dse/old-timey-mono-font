function initCodeVariantCheckbox() {
    var checkbox = document.getElementById("code-checkbox");
    var element = (document.getElementById("whole-char-list") ||
                   document.getElementById("whole-char-grid"));
    if (!element) {
        return;
    }
    checkbox.addEventListener("change", update);
    var checked = JSON.parse(localStorage.getItem("old-timey-codeCheckboxChecked"));
    console.log(checked);
    checkbox.checked = checked;
    function update() {
        if (checkbox.checked) {
            element.classList.add("code");
            localStorage.setItem("old-timey-codeCheckboxChecked", "true");
            console.log("true");
        } else {
            element.classList.remove("code");
            localStorage.setItem("old-timey-codeCheckboxChecked", "false");
            console.log("false");
        }
    }
}

if (document.readyState === 'complete') {
    initCodeVariantCheckbox();
} else {
    window.addEventListener('load', initCodeVariantCheckbox);
}
