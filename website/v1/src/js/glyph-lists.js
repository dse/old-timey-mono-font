/*global categoriesData, glyphsData, fontGlyphsData */
/*jshint ignore: start */
import categoriesData from "../../../../src/data/external/category-data.json" with { type: "json" };
import glyphsData     from "../../../../src/data/external/glyph-data.json"    with { type: "json" };
import fontGlyphsData from "../../../../src/data/glyphs-data.json"            with { type: "json" };
/*jshint ignore: end */

import _ from "lodash";

const fontGlyphCodepoints = [...new Set(fontGlyphsData.glyphs.map(g => g.unicode))].filter(x => x >= 0).sort();

export default function getGlyphLists() {
    const lists = [];
    const categoryNames = Object.keys(categoriesData);
    glyphsData.forEach(glyphData => {
        if (glyphData.unicode != null) {
            const code = parseInt(glyphData.unicode, 16);
            const char = String.fromCodePoint(code);
            glyphData.decimal = code;
            glyphData.char = char;
            if (fontGlyphCodepoints.includes(code)) {
                glyphData.data = fontGlyphsData.glyphs.filter(g => g.unicode === code && g.isBaseGlyph)[0];
            }
        }
    });
    categoryNames.forEach(categoryName => {
        const categoryGlyphs = glyphsData.filter(g => g.category === categoryName && fontGlyphCodepoints.includes(g.decimal));
        const subCategoryNames = [...new Set(categoryGlyphs.map(g => g.subCategory).filter(x => x != null))];
        subCategoryNames.forEach(subCategoryName => {
            const subCategoryGlyphs = categoryGlyphs.filter(g => g.subCategory === subCategoryName);
            if (!subCategoryGlyphs.length) {
                return;
            }
            const scripts = [...new Set(subCategoryGlyphs.map(g => g.script).filter(x => x != null))];
            scripts.forEach(script => {
                const glyphs = subCategoryGlyphs.filter(g => g.script === script);
                lists.push({
                    "name": `${categoryName} ${subCategoryName} ${_.startCase(script)}`,
                    glyphs: glyphs
                });
            });
            const otherGlyphs = subCategoryGlyphs.filter(g => !scripts.includes(g.script));
            if (otherGlyphs.length) {
                lists.push({
                    "name": `${categoryName} ${subCategoryName} - other`,
                    "glyphs": otherGlyphs,
                });
            }
        });
        const otherGlyphs = categoryGlyphs.filter(g => !subCategoryNames.includes(g.subCategory));
        if (otherGlyphs.length) {
            lists.push({
                "name": `${categoryName} - other`,
                "glyphs": otherGlyphs,
            });
        }
    });
    const otherGlyphs = glyphsData.filter(g => !categoryNames.includes(g.category));
    if (otherGlyphs.length) {
        lists.push({
            "name": "Other",
            "glyphs": otherGlyphs,
        });
    }
    return lists;
}
