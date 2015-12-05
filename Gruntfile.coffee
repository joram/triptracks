
module.exports = (grunt) ->

  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    coffee:
      compile:
        expand: true
        cwd: "trip_planner_www/common"
        src: ["static/coffee/*.coffee"]
        dest: 'static/generated-js/'
        ext: ".js"
        options:
          bare: true
          preserve_dirs: true

    watch:
      coffee:
        files: 'trip_planner_www/**/*.coffee'
        tasks: ['coffee']
      options:
        livereload: true

  #Load Tasks
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  grunt.registerTask 'coffee', ['coffee']
  grunt.registerTask 'watch', ['coffee']
  grunt.registerTask 'default', ['watch']
