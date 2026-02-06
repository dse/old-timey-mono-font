import gulp from "gulp";

import {
    setDevModeTask,
    setProdModeTask,
    initTask,
    rollupTask,
    sassTask,
    htmlTask,
    serverTask,
    watchTask,
    copyStaticFilesTask,
    config,
} from "./chug/gulpfile.js";

const devTask = gulp.series(
    setDevModeTask,
    initTask,
    function (cb) {
        config.browserSync = {
            serveStatic: [
                "dist",
                "public",
                {
                    dir: "../../dist/ttf",
                    route: "/fonts",
                },
            ],
            logLevel: "debug",
        };
        cb?.();
    },
    copyStaticFilesTask,
    gulp.parallel(
        rollupTask,
        sassTask,
        htmlTask,
    ),
    serverTask,
    watchTask,
);

const buildTask = gulp.series(
    setProdModeTask,
    initTask,
    copyStaticFilesTask,
    gulp.parallel(
        rollupTask,
        sassTask,
        htmlTask,
    ),
);

export {
    devTask as dev,
    buildTask as build,
};
