import gulp from "gulp";

import { sassTask } from "./chug/gulp/sass.js";
import { nunjucksTask } from "./chug/gulp/nunjucks.js";
import { startServerTask } from "./chug/gulp/server.js";
import { watchSassTask, watchNunjucksTask } from "./chug/gulp/watch.js";
import { registerSiteData } from "./chug/gulp/site-data.js";
import { addManageEnvCallback } from "./chug/gulp/nunjucks.js";

import { getFontData, ord, chr, charname, uhex } from "./src/scripts/unicode.js";

const fontData = getFontData("../../dist/ttf/OldTimeyMono.ttf");
registerSiteData("fontData", fontData);

addManageEnvCallback(function (env) {
    env.addFilter("ord", ord);
    env.addFilter("chr", chr);
    env.addFilter("charname", charname);
    env.addFilter("uhex", uhex);
});

function copyFontsTask() {
    return gulp.src(["../../dist/ttf/OldTimeyCode.ttf",
                     "../../dist/ttf/OldTimeyMono.ttf"], { encoding: false })
               .pipe(gulp.dest("dist/web/fonts"));
}

const devTask = gulp.series(
    copyFontsTask,
    gulp.parallel(
        sassTask,
        nunjucksTask,
    ),
    startServerTask,
    watchSassTask,
    watchNunjucksTask,
);

const buildTask = gulp.series(
    copyFontsTask,
    gulp.parallel(
        sassTask,
        nunjucksTask,
    ),
);

export {
    devTask as dev,
    buildTask as build,
};
