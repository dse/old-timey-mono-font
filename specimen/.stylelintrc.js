module.exports = {
	extends: ["stylelint-config-standard", "stylelint-config-prettier"],
	plugins: ["stylelint-no-unsupported-browser-features"],
	rules: {
		"selector-id-pattern": [
			"^([a-z][a-z0-9]*)(-[a-z0-9]+)*$",
			{
				message:
					"Selector should use lowercase and separate words with hyphens (selector-class-pattern)"
			}
		],
		"selector-class-pattern": [
			"^([a-z][a-z0-9]*)(-[a-z0-9]+)*$",
			{
				message:
					"Selector should use lowercase and separate words with hyphens (selector-class-pattern)"
			}
		],
		indentation: "tab",
		"selector-pseudo-class-no-unknown": [
			true,
			{
				ignorePseudoClasses: ["global"]
			}
		],
		"plugin/no-unsupported-browser-features": [
			true,
			{
				severity: "warning",
				ignore: ["font-unicode-range", "css-resize", "css-appearance"]
			}
		]
	}
};
