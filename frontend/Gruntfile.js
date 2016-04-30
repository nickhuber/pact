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
        files: ['src/less/*.less', 'bower_components/angular-xeditable/dist/css/xeditable.css'],
        tasks: ['less', 'concat']
      },
      fonts: {
        files: ['bower_components/bootstrap/fonts/*'],
        tasks: ['copy']
      }
    },
    less: {
      development: {
        files: {
          'build/css/standard.css': 'src/less/standard.less',
          'build/css/xeditable.css': 'bower_components/angular-xeditable/dist/css/xeditable.css',
          'build/css/loading-bar.css': 'bower_components/angular-loading-bar/build/loading-bar.css',
        }
      }
    },
    concat: {
      js: {
        options: {
          separator: ';\n'
        },
        src: [
          'bower_components/jquery/dist/jquery.js',
          'bower_components/underscore/underscore.js',
          'bower_components/angularjs/angular.js',
          'bower_components/angular-resource/angular-resource.js',
          'bower_components/angular-route/angular-route.js',
          'bower_components/angular-xeditable/dist/js/xeditable.js',
          'bower_components/angular-loading-bar/build/loading-bar.js',
          'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
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
      fonts: {src: ['bower_components/bootstrap/fonts/*'], dest: 'app/fonts/', flatten: true, expand: true}
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
      'copy',
    ]
  );
}
