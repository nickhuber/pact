module.exports = function(grunt) {

  grunt.initConfig({
    watch: {
      javascript: {
        files: ['src/js/*.js'],
        tasks: ['concat']
      },
      main: {
        files: ['src/index.html'],
        tasks: ['copy']
      },
      partials: {
        files: ['src/partials/*.html'],
        tasks: ['copy']
      },
      less: {
        files: ['src/less/*.less'],
        tasks: ['less', 'concat']
      },
      fonts: {
        files: ['bower_components/components-font-awesome/fonts/*'],
        tasks: ['copy']
      }
    },
    less: {
      development: {
        files: {
          'build/css/standard.css': 'src/less/standard.less'
        }
      }
    },
    concat: {
      js: {
        options: {
          separator: ';\n'
        },
        src: [
          'bower_components/angularjs/angular.js',
          'bower_components/angular-resource/angular-resource.js',
          'bower_components/angular-route/angular-route.js',
          'bower_components/jquery/dist/jquery.js',
          'bower_components/underscore/underscore.js',
          'src/js/*.js'
        ],
        dest: 'app/js/combat_tracker.js',
      },
      css: {
        src: 'build/css/*.css',
        dest: 'app/css/combat_tracker.css'
      }
    },
    copy: {
      main: {src: ['src/index.html'], dest: 'app/index.html'},
      partials: {src: ['src/partials/*.html'], dest: 'app/partials/', flatten: true, expand: true},
      fonts: {src: ['bower_components/components-font-awesome/fonts/*'], dest: 'app/fonts/', flatten: true, expand: true}
    }
  });

  // Load plugins here
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default',
    [
      'less',
      'concat',
      'copy'
    ]
  );
}
