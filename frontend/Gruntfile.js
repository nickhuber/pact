module.exports = function(grunt) {

  grunt.initConfig({
    watch: {
      javascript: {
        files: ['src/js/*.js'],
        tasks: ['concat', 'uglify']
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
        tasks: ['less', 'concat', 'cssmin']
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
          'build/css/xeditable.css': 'bower_components/angular-xeditable/dist/css/xeditable.css'
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
    },
    uglify: {
      options: {
        mangle: false
      },
      main: {
        files: {
            'app/js/combat_tracker.min.js': ['app/js/combat_tracker.js']
        }
      }
    },
    cssmin: {
      main: {
        files: {
          'app/css/combat_tracker.min.css': ['app/css/combat_tracker.css']
        }
      }
    }

  });

  // Load plugins here
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

  grunt.registerTask('default',
    [
      'less',
      'concat',
      'copy',
      'cssmin',
      'uglify',
    ]
  );
}
