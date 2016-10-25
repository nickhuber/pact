module.exports = function(grunt) {
    grunt.initConfig({
        watch: {
            javascript: {
                files: ['src/js/*.js'],
                tasks: ['concat', 'clean:js', 'copy', 'cacheBust']
            },
            templates: {
                files: ['src/templates/*.html'],
                tasks: ['ngtemplates', 'concat', 'clean:js', 'copy', 'cacheBust']
            },
            main: {
                files: ['src/index.html'],
                tasks: ['copy:main', 'clean:js', 'copy', 'cacheBust',]
            },
            less: {
                files: ['src/less/*.less'],
                tasks: ['less', 'cssmin', 'clean:css', 'copy', 'cacheBust']
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
                    'bower_components/marked/marked.min.js',
                    'bower_components/bootstrap/dist/js/bootstrap.min.js',
                    'bower_components/underscore/underscore-min.js',
                    'bower_components/angular/angular.min.js',
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
                dest: 'app/js/pact.js',
            },
        },
        cssmin: {
            target: {
                files: {
                    'app/css/pact.css': ['build/css/*.css']
                }
            }
        },
        copy: {
            main: {src: ['src/index.html'], dest: 'app/index.html'},
            fonts: {src: ['bower_components/bootstrap/fonts/*'], dest: 'app/fonts/', flatten: true, expand: true}
        },
        ngtemplates: {
            PACT: {
                cwd: 'src',
                src: 'templates/*.html',
                dest: 'build/js/templates.js'
            }
        },
        clean: {
            js: ['app/js/*.js', '!app/js/pact.js'],
            css: ['app/css/*.css', '!app/css/pact.css']
        },
        cacheBust: {
            options: {
                assets: ['css/pact.css', 'js/pact.js'],
                baseDir: 'app/'
            },
            main: {
                files: [{
                    expand: true,
                    cwd: 'app/',
                    src: ['index.html']
                }]
            }
        }
    });

    // Load plugins here
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-cache-bust');

    grunt.registerTask('default', [
        'ngtemplates',
        'less',
        'cssmin',
        'concat',
        'copy',
        'clean',
        'cacheBust',
    ]);
};
