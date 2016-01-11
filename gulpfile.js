
var gulp = require('gulp');
var coffee = require('gulp-coffee');

function swallowError (error) {
  console.log(error.toString());
  this.emit('end');
}

gulp.task('common-coffee-to-js', function(){
    return gulp.src('trip_planner_www/common/static/coffee/*.coffee')
        .pipe(coffee())
        .on('error', swallowError)
        .pipe(gulp.dest('trip_planner_www/common/static/compiled-js/'));
});

gulp.task('coffee', function(){
    gulp.watch('trip_planner_www/common/static/coffee/*.coffee', ['common-coffee-to-js']);
});