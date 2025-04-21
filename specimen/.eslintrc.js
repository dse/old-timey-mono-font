module.exports = {
	plugins: ["prettier"],
	extends: ["eslint:recommended", "plugin:node/recommended"],
	rules: {
		"prettier/prettier": "error",
		"node/no-unpublished-require": "off"
	}
};
