const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ManifestPlugin = require("webpack-manifest-plugin");

const env = process.env.NODE_ENV || "development";
const isProd = env === "production";
const input = path.resolve(__dirname, "src");
const out = path.resolve(__dirname, "_site");
const exclusions = /node_modules/;

const inlineImgLimit = 8192;

const optimization = {
	splitChunks: isProd && { chunks: "all" },
	minimize: isProd,
	// prints more readable module names in the browser console on HMR updates, in dev
	namedModules: !isProd,
	// prevent emitting assets with errors, in dev
	noEmitOnErrors: !isProd
};

const fileLoaderOptions = {
	name: "[path][name].[hash].[ext]",
	context: input
};

module.exports = {
	mode: isProd ? "production" : "development",
	entry: {
		main: [
			path.resolve(input, "js", "main.js"),
			path.resolve(input, "css", "main.css")
		]
	},
	output: {
		path: out,
		filename: "[name].[hash].js",
		publicPath: "./"
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: exclusions,
				use: {
					loader: "babel-loader",
					options: {
						presets: ["@babel/preset-env"]
					}
				}
			},
			{
				test: /\.css$/,
				exclude: exclusions,
				use: [
					{
						loader: MiniCssExtractPlugin.loader
					},
					"css-loader",
					"postcss-loader"
				]
			},
			{
				include: path.resolve(input, "fonts"),
				use: [
					{
						loader: "file-loader",
						options: fileLoaderOptions
					}
				]
			},
			{
				test: /\.svg$/i,
				oneOf: [
					{
						resourceQuery: /external/,
						loader: "file-loader",
						options: fileLoaderOptions
					},
					{
						resourceQuery: /inline/,
						loader: "svg-url-loader",
						options: fileLoaderOptions
					},
					{
						loader: "svg-url-loader",
						options: {
							...fileLoaderOptions,
							limit: inlineImgLimit
						}
					}
				]
			},
			{
				test: /\.(png|jpg)$/i,
				oneOf: [
					{
						resourceQuery: /external/,
						loader: "file-loader",
						options: fileLoaderOptions
					},
					{
						resourceQuery: /inline/,
						loader: "url-loader",
						options: {
							...fileLoaderOptions,
							limit: true
						}
					},
					{
						loader: "url-loader",
						options: {
							...fileLoaderOptions,
							limit: inlineImgLimit
						}
					}
				]
			}
		]
	},
	devtool: isProd ? false : "eval",
	optimization,
	plugins: [
		new MiniCssExtractPlugin({
			filename: "styles.[contenthash].css",
			ignoreOrder: false
		}),
		new ManifestPlugin({
			fileName: path.resolve(
				input,
				"_includes",
				".webpack",
				"manifest.json"
			),
			map: file => {
				switch (file.name) {
					case "main.js":
						file.name = "js/main.js";
						break;
					case "main.css":
						file.name = "css/main.css";
						break;
					default:
						// Strip queries like ?external from asset name
						file.name = file.name.split("?")[0];
				}

				return file;
			}
		})
	]
};
