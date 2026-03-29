import {
    buildTask, devTask,
    sassTask, cleanTask, initTask,
    nunjucksTask, rollupTask, staticTask,
    startServerTask,
    watchTask,
    buildSeriesTask,
    devSeriesTask,
} from "../../chug/index.js";

buildSeriesTask.displayName = "build:series";
devSeriesTask.displayName = "dev:series";

export {
    buildTask as build,
    devTask as dev,
    cleanTask as clean,
    initTask as init,
    sassTask as sass,
    nunjucksTask as nunjucks,
    rollupTask as rollup,
    staticTask as static,
    startServerTask as server,
    watchTask as watch,
    buildSeriesTask as buildSeries,
    devSeriesTask as devSeries,
};

// export const exports = {
//     build:          buildTask,
//     dev:            devTask,
//     clean:          cleanTask,
//     init:           initTask,
//     sass:           sassTask,
//     nunjucks:       nunjucksTask,
//     rollup:         rollupTask,
//     static:         staticTask,
//     server:         startServerTask,
//     watch:          watchTask,
//     "build:series": buildSeriesTask,
//     "dev:series":   devSeriesTask,
// };
// export default exports;
