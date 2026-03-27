/*global fontData, fontGlyphsData */

import gulp from "gulp";
import * as sassImpl from "sass";
import gulpSass from "gulp-sass";
import nunjucks from "gulp-nunjucks-render";
import beautify from "gulp-beautify";
import data from "gulp-data";
import { Transform } from "node:stream";
import browserSync from "browser-sync";

import getGlyphLists from "./src/js/glyph-lists.js";

const htmlData = {
    glyphLists: getGlyphLists(),
};

const sass = gulpSass(sassImpl);

const EXCLUDE_PARTIALS = [
    "!**/_*",
    "!**/_*/**/*",
];
const EXCLUDE_TEMP = [
    "!**/*.tmp",
    "!**/*~",
    "!**/#*#",
];
const COMPILE_EXCLUDE = [
    ...EXCLUDE_PARTIALS,
    ...EXCLUDE_TEMP,
];
const WATCH_EXCLUDE = [
    ...EXCLUDE_TEMP,
];

function wroteWriter() {
    return new Transform({
        objectMode: true,
        transform(file, enc, callback) {
            console.log(`Wrote ${file.path}`);
            callback(null, this);
        },
    });
}

function sassTask() {
    return gulp.src(["src/styles/*.scss", ...COMPILE_EXCLUDE])
               .pipe(sass({
                   quietDeps: true,
                   silenceDeprecations: [
                       "import",
                   ],
               }))
               .pipe(gulp.dest("dist/css"))
               .pipe(wroteWriter());
}

let resetHtmlLastRunFlag = true;

function htmlTask() {
    const since = resetHtmlLastRunFlag ? {} : { since: gulp.lastRun(htmlTask) };
    resetHtmlLastRunFlag = false;
    return gulp.src(["src/html/**/*.njk", ...COMPILE_EXCLUDE], since)
               .pipe(data(_ => htmlData))
               .pipe(nunjucks({ path: "src/html" }))
               .pipe(beautify.html())
               .pipe(gulp.dest("dist"))
               .pipe(wroteWriter());
}

function resetHtmlLastRun(cb) {
    resetHtmlLastRunFlag = true;
    cb?.();
}

let server;

function startTask(cb) {
    if (server) {
        cb?.();
        return;
    }
    server = browserSync.create();
    server.init({
        server: "./dist",
    }, cb);
}

function reloadTask(cb) {
    if (server) {
        server.reload();
    }
    cb?.();
}

function watchTask() {

    const watchSass = ["src/styles/**/*",
                       ...WATCH_EXCLUDE];
    const watchHtml = ["src/html/**/*",
                       ...EXCLUDE_PARTIALS,
                       ...WATCH_EXCLUDE];
    const watchHtmlPartials = ["src/html/**/_*",
                               "src/html/**/_*/**/*",
                               ...WATCH_EXCLUDE];

    console.log(`Watching ${JSON.stringify(watchSass)}`);
    gulp.watch(watchSass, gulp.series(sassTask, reloadTask));
    console.log(`Watching ${JSON.stringify(watchHtml)}`);
    gulp.watch(watchHtml, gulp.series(htmlTask, reloadTask));
    console.log(`Watching ${JSON.stringify(watchHtmlPartials)}`);
    gulp.watch(watchHtmlPartials, gulp.series(resetHtmlLastRun, htmlTask, reloadTask));
}

const buildTask = gulp.parallel(
    sassTask,
    htmlTask,
);

const devTask = gulp.series(
    buildTask,
    startTask,
    watchTask,
);

export { devTask as dev };
export { buildTask as build };
export { sassTask as sass };
export { htmlTask as html };
export default buildTask;
