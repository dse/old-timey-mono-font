const fs = require("fs");
const path = require("path");
const util = require("util");
const readFile = util.promisify(fs.readFile);
const htmlmin = require("html-minifier");

const inputDir = path.resolve(__dirname, "./src");

const webpackAssetPath = async name => {
	const manifestData = await readFile(
		path.resolve(inputDir, "_includes", ".webpack", "manifest.json")
	);
	const manifest = JSON.parse(manifestData);

	const assetPath = manifest[name];
	if (assetPath == null) {
		throw new Error(
			`Unknown Webpack asset requested: ${name}. Check .webpack/manifest.json.`
		);
	}

	return assetPath;
};

const webpackAssetContents = async name => {
	const assetName = await webpackAssetPath(name);
	const filePath = path.resolve(__dirname, "_site", assetName);

	return readFile(filePath);
};

const relativePathTag = processPath => liquidEngine => {
	return {
		parse: function(tagToken) {
			this.arg = tagToken.args;
			this.templateFile = tagToken.file;
		},
		render: async function(scope) {
			const fileParam =
				liquidEngine.evalValue(this.arg, scope) || this.arg;

			const resolvedFile = path.resolve(
				path.dirname(this.templateFile),
				fileParam
			);

			const srcRelativePath = path.relative(inputDir, resolvedFile);
			return processPath(srcRelativePath);
		}
	};
};

module.exports = eleventyConfig => {
	eleventyConfig.setUseGitIgnore(false);

	eleventyConfig.addFilter("json_stringify", JSON.stringify);

	eleventyConfig.addLiquidTag(
		"webpackAssetPath",
		relativePathTag(webpackAssetPath)
	);
	eleventyConfig.addLiquidTag(
		"includeWebpackAsset",
		relativePathTag(webpackAssetContents)
	);

	if (process.env.ELEVENTY_ENV === "production") {
		eleventyConfig.addTransform("htmlmin", (content, outputPath) => {
			if (outputPath.endsWith(".html")) {
				let minified = htmlmin.minify(content, {
					useShortDoctype: true,
					removeComments: true,
					collapseWhitespace: true
				});
				return minified;
			}

			return content;
		});
	}

	return {
		dir: {
			input: "./src",
			layouts: "_layouts"
		}
	};
};
