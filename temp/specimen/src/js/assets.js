/**
 * This file automatically requires every supported image in `src/img`.
 */
const requireAll = r => r.keys().forEach(r);
requireAll(require.context("../img/?external", true, /\.(png|jpg|svg)$/));
