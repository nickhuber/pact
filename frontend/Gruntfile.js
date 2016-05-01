module.exports = function(grunt) {
    grunt.initConfig({
        watch: {
            javascript: {
                files: ['src/js/*.js'],
                tasks: ['concat', 'cachebreaker']
            },
            templates: {
                files: ['src/partials/*.html'],
                tasks: ['ngtemplates', 'concat', 'cachebreaker']
            },
            main: {
                files: ['src/index.html'],
                tasks: ['copy', 'cachebreaker',]
            },
            less: {
                files: ['src/less/*.less'],
                tasks: ['less', 'cssmin', 'cachebreaker']
            },
        },
        less: {
            development: {
                files: {
                    'build/css/standard.css': 'src/less/*.less',
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
                    'bower_components/jquery/dist/jquery.min.js',
                    'bower_components/marked/lib/marked.js',
                    'bower_components/bootstrap/dist/js/bootstrap.min.js',
                    'bower_components/underscore/underscore-min.js',
                    'bower_components/angularjs/angular.min.js',
                    'bower_components/angular-resource/angular-resource.min.js',
                    'bower_components/angular-route/angular-route.min.js',
                    'bower_components/angular-animate/angular-animate.min.js',
                    'bower_components/angular-xeditable/dist/js/xeditable.min.js',
                    'bower_components/angular-loading-bar/build/loading-bar.min.js',
                    'bower_components/angular-marked/dist/angular-marked.min.js',
                    'bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
                    'src/js/*.js',
                    'build/js/templates.js',
                ],
                dest: 'app/js/combat_tracker.js',
            },
        },
        cssmin: {
            target: {
                files: {
                    'app/css/combat_tracker.css': ['build/css/*.css']
                }
            }
        },
        copy: {
            main: {src: ['src/index.html'], dest: 'app/index.html'},
            fonts: {src: ['bower_components/bootstrap/fonts/*'], dest: 'app/fonts/', flatten: true, expand: true}
        },
        ngtemplates: {
            combatTracker: {
                cwd: 'src',
                src: 'partials/*.html',
                dest: 'build/js/templates.js'
            }
        },
        cachebreaker: {
            dev: {
                options: {
                    match: [
                        {
                            'combat_tracker.js': 'app/js/combat_tracker.js',
                            'combat_tracker.css': 'app/css/combat_tracker.css',
                        }
                    ],
                    replacement: 'md5',
                },
                files: {
                    src: ['app/index.html']
                }
            }
        }

    });

    // Load plugins here
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-cache-breaker');

    grunt.registerTask('default', [
        'ngtemplates',
        'less',
        'cssmin',
        'concat',
        'copy',
        'cachebreaker',
    ]);
};
