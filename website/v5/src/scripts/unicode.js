import latinCodepoints                          from "@unicode/unicode-17.0.0/Script/Latin/code-points.js";
import cyrillicCodepoints                       from "@unicode/unicode-17.0.0/Script/Cyrillic/code-points.js";
import greekCodepoints                          from "@unicode/unicode-17.0.0/Script/Greek/code-points.js";
import generalCategories                        from "@unicode/unicode-17.0.0/General_Category/index.js";
import charNames                                from "@unicode/unicode-17.0.0/Names/index.js";

import blockElementsBlock                       from "@unicode/unicode-17.0.0/Block/Block_Elements/code-points.js";
import boxDrawingBlock                          from "@unicode/unicode-17.0.0/Block/Box_Drawing/code-points.js";
import braillePatternsBlock                     from "@unicode/unicode-17.0.0/Block/Braille_Patterns/code-points.js";
import symbolsForLegacyComputingBlock           from "@unicode/unicode-17.0.0/Block/Symbols_For_Legacy_Computing/code-points.js";
import symbolsForLegacyComputingSupplementBlock from "@unicode/unicode-17.0.0/Block/Symbols_For_Legacy_Computing_Supplement/code-points.js";
import ipaExtensionsBlock                       from "@unicode/unicode-17.0.0/Block/IPA_Extensions/code-points.js";

import * as fontkit from "fontkit";

export function getFontData(filename) {
    let font = fontkit.openSync(filename);
    const symbols = {
        latin: {
            alpha: [],
            mark: [],
            nonAlpha: [],
        },
        greek: {
            alpha: [],
            mark: [],
            nonAlpha: [],
        },
        cyrillic: {
            alpha: [],
            mark: [],
            nonAlpha: [],
        },
        numeric: [],
        punct: [],
        symbol: [],
        space: [],
        mark: [],
        other: [],
        box: [],
        braille: [],
        block: [],
        legacy: [],
        ipa: [],

        category: {},
        otherCategory: {},
    };
    const codepoints = font.characterSet;
    codepoints.sort((a, b) => a - b);
    for (const codepoint of codepoints) {
        // controls
        if (codepoint < 32 || (codepoint >= 127 && codepoint <= 159)) {
            continue;
        }

        // soft hyphen
        if (codepoint === 0x00ad) {
            continue;
        }

        // private use and surrogates
        if (codepoint >= 0xd800   && codepoint <= 0xdfff  ) { continue; }
        if (codepoint >= 0xe000   && codepoint <= 0xf8ff  ) { continue; }
        if (codepoint >= 0xf0000  && codepoint <= 0xfffff ) { continue; }
        if (codepoint >= 0x100000 && codepoint <= 0x10ffff) { continue; }

        const isLatin = latinCodepoints.includes(codepoint);
        const isGreek = greekCodepoints.includes(codepoint);
        const isCyrillic = cyrillicCodepoints.includes(codepoint);
        const generalCategory = generalCategories.get(codepoint);

        const isIpa = ipaExtensionsBlock.includes(codepoint);
        const isBoxDrawing = boxDrawingBlock.includes(codepoint);
        const isBraille = braillePatternsBlock.includes(codepoint);
        const isBlock = blockElementsBlock.includes(codepoint);
        const isLegacy = symbolsForLegacyComputingBlock.includes(codepoint) || symbolsForLegacyComputingSupplementBlock.includes(codepoint);

        const isAlpha = [
            "Lu", "Uppercase_Letter",
            "Ll", "Lowercase_Letter",
            "Lt", "Titlecase_Letter",
            "LC", "Cased_Letter",
            "Lm", "Modifier_Letter",
            "Lo", "Other_Letter",
            "L", "Letter",
        ].includes(generalCategory);
        const isMark = [
            "Mn", "Nonspacing_Mark",
            "Mc", "Spacing_Mark",
            "Me", "Enclosing_Mark",
            "M", "Mark",
        ].includes(generalCategory);
        const isNumeric = [
            "Nd", "Decimal_Number",
            "Nl", "Letter_Number",
            "No", "Other_Number",
            "N", "Number",
        ].includes(generalCategory);
        const isPunct = [
            "Pc", "Connector_Punctuation",
            "Pd", "Dash_Punctuation",
            "Ps", "Open_Punctuation",
            "Pe", "Close_Punctuation",
            "Pi", "Initial_Punctuation",
            "Pf", "Final_Punctuation",
            "Po", "Other_Punctuation",
            "P", "Punctuation",
        ].includes(generalCategory);
        const isSymbol = [
            "Sm", "Math_Symbol",
            "Sc", "Currency_Symbol",
            "Sk", "Modifier_Symbol",
            "So", "Other_Symbol",
            "S", "Symbol",
        ].includes(generalCategory);
        const isSeparator = [
            "Zs", "Space_Separator",
            "Zl", "Line_Separator",
            "Zp", "Paragraph_Separator",
            "Z", "Separator",
        ].includes(generalCategory);
        const isOther = [
            "Cc", "Control",
            "Cf", "Format",
            "Cs", "Surrogate",
            "Co", "Private_Use",
            "Cn", "Unassigned",
            "C", "Other",
        ].includes(generalCategory);
        if (isIpa) {
            symbols.ipa.push(codepoint);
        }
        if (isLatin) {
            if (isAlpha) {
                symbols.latin.alpha.push(codepoint);
            } else if (isMark) {
                symbols.latin.mark.push(codepoint);
            } else {
                symbols.latin.nonAlpha.push(codepoint);
            }
        } else if (isGreek) {
            if (isAlpha) {
                symbols.greek.alpha.push(codepoint);
            } else if (isMark) {
                symbols.greek.mark.push(codepoint);
            } else {
                symbols.greek.nonAlpha.push(codepoint);
            }
        } else if (isCyrillic) {
            if (isAlpha) {
                symbols.cyrillic.alpha.push(codepoint);
            } else if (isMark) {
                symbols.cyrillic.mark.push(codepoint);
            } else {
                symbols.cyrillic.nonAlpha.push(codepoint);
            }
        } else if (isBlock) {
            symbols.block.push(codepoint);
        } else if (isBoxDrawing) {
            symbols.box.push(codepoint);
        } else if (isBraille) {
            symbols.braille.push(codepoint);
        } else if (isLegacy) {
            symbols.legacy.push(codepoint);
        } else if (isPunct) {
            symbols.punct.push(codepoint);
        } else if (isNumeric) {
            symbols.numeric.push(codepoint);
        } else if (isSeparator) {
            symbols.space.push(codepoint);
        } else if (isMark) {
            symbols.mark.push(codepoint);
        } else if (isSymbol) {
            symbols.symbol.push(codepoint);
        } else {
            const otherCategoryName = generalCategory.replace(/_/g, " ");
            symbols.otherCategory[otherCategoryName] = symbols.otherCategory[otherCategoryName] ?? [];
            symbols.otherCategory[otherCategoryName].push(codepoint);
            symbols.other.push(codepoint);
        }
        const generalCategoryName = generalCategory.replace(/_/g, " ");
        symbols.category[generalCategoryName] = symbols.category[generalCategoryName] ?? [];
        symbols.category[generalCategoryName].push(codepoint);
    }
    return symbols;
}

function parseChar(str) {
    str = String(str);
    let match;
    if ((match = /^(?:u\+?|0?x)([0-9A-Fa-f]+)$/.exec(str))) {
        return parseInt(match[1], 16);
    }
    if (/^\d+$/.test(str)) {
        return parseInt(str, 10);
    }
    if (str.length === 1) {
        return str.codePointAt(0);
    }
    return null;
}

export function ord(str) {
    return str.codePointAt(0);
}
export function chr(codepoint) {
    return String.fromCodePoint(codepoint);
}
export function uhex(str) {
    const code = parseChar(str);
    if (code == null) {
        return "(none)";
    }
    const result = code.toString(16).toUpperCase();
    return "U+" + result.padStart(4, '0');
}
export function charname(str) {
    const code = parseChar(str);
    if (code == null) {
        return "(none)";
    }
    return charNames.get(code) ?? "(none)";
}
