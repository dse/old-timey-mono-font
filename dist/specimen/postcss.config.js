const cssnano = () => {
	return require("cssnano")({
		preset: "default"
	});
};

module.exports = {
	plugins: [
		require("postcss-import"),
		require("autoprefixer"),
		process.env.NODE_ENV === "production" ? cssnano() : false
	]
};
