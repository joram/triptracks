
var gulp = require('gulp');
var coffee = require('gulp-coffee');

gulp.task('common-coffee-to-js', function(){
    return gulp.src('trip_planner_www/common/static/coffee/*.coffee')
        .pipe(coffee())
        .pipe(gulp.dest('trip_planner_www/common/static/compiled-js/'));
});

gulp.task('coffee', function(){
    gulp.watch('trip_planner_www/common/static/coffee/*.coffee', ['common-coffee-to-js']);
});