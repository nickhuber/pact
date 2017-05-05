
CLEANCSS_CMD = ./node_modules/.bin/cleancss
MD5_CMD = ./md5.sh

BUILD_DIR = build
JS_BUILD_DIR = $(BUILD_DIR)/js
CSS_BUILD_DIR = $(BUILD_DIR)/css
DIST_DIR = dist
JS_DIST_DIR = $(DIST_DIR)/js
CSS_DIST_DIR = $(DIST_DIR)/css
FONTS_DIR = $(DIST_DIR)/fonts

source_js_files := $(wildcard src/js/*.js)

angular_templates = $(patsubst src/templates/%.html,$(BUILD_DIR)/js/templates.%.js,$(wildcard src/templates/*.html))

fonts = $(wildcard node_modules/font-awesome/fonts/*)
moved_fonts = $(patsubst node_modules/font-awesome/fonts/%,$(DIST_DIR)/fonts/%,$(wildcard node_modules/font-awesome/fonts/*))

extern_js_libraries := node_modules/jquery/dist/jquery.min.js \
	node_modules/marked/marked.min.js \
	node_modules/bootstrap-sass/assets/javascripts/bootstrap.min.js \
	node_modules/underscore/underscore-min.js \
	node_modules/angular/angular.min.js \
	node_modules/angular-resource/angular-resource.min.js \
	node_modules/angular-route/angular-route.min.js \
	node_modules/angular-animate/angular-animate.min.js \
	node_modules/angular-xeditable/dist/js/xeditable.min.js \
	node_modules/angular-loading-bar/build/loading-bar.min.js \
	node_modules/angular-marked/dist/angular-marked.min.js \
	node_modules/angular-ui-bootstrap/dist/ui-bootstrap-tpls.js


external_css_libraries := node_modules/font-awesome/css/font-awesome.min.css \
	node_modules/angular-xeditable/dist/css/xeditable.css \
	node_modules/angular-loading-bar/build/loading-bar.css

.PHONY: all clean cachebust-js cachebust-css

all: $(DIST_DIR)/index.html $(moved_fonts)


# Javascript
$(BUILD_DIR)/js/pact.js: $(extern_js_libraries) $(source_js_files) $(angular_templates) $(JS_BUILD_DIR)/.d
	rm -f $@
	for f in $^ ; do (cat "$$f" ; echo ';') >> $@ ; done

$(BUILD_DIR)/js/templates.%.js: src/templates/%.html $(JS_BUILD_DIR)/.d
	./ng-compile-templates.py $< PACT $@

$(BUILD_DIR)/js/templates.js: $(BUILD_DIR)/js/templates.*.js $(JS_BUILD_DIR)/.d
	cat $^ > $@

cachebust-js: $(BUILD_DIR)/js/pact.js $(JS_DIST_DIR)/.d
	rm -f $(DIST_DIR)/js/pact.*.js
	cp $< $(DIST_DIR)/js/pact.$(shell $(MD5_CMD) $<).js


# CSS
$(BUILD_DIR)/css/pact-internal.css: src/stylesheets/pact.scss $(CSS_BUILD_DIR)/.d
	sassc $< $@
	$(CLEANCSS_CMD) $@ -o $@

$(BUILD_DIR)/css/pact.css: $(external_css_libraries) $(BUILD_DIR)/css/pact-internal.css $(CSS_BUILD_DIR)/.d
	rm -f $@
	for f in $^ ; do (cat "$$f" ; echo ';') >> $@ ; done

cachebust-css: $(BUILD_DIR)/css/pact.css $(CSS_DIST_DIR)/.d
	rm -f $(DIST_DIR)/css/pact.*.css
	cp $< $(DIST_DIR)/css/pact.$(shell $(MD5_CMD) $<).css


# Fonts
$(DIST_DIR)/fonts/%: node_modules/font-awesome/fonts/% $(FONTS_DIR)/.d
	cp $< $@


# HTML
# TODO: make this not run every time
$(DIST_DIR)/index.html: src/index.html $(DIST_DIR)/.d cachebust-css cachebust-js
	cp $< $@
ifeq ($(shell uname),Darwin)
	sed -i '' 's/pact.js/pact.$(shell $(MD5_CMD) $(BUILD_DIR)/js/pact.js).js/' $@
	sed -i '' 's/pact.css/pact.$(shell $(MD5_CMD) $(BUILD_DIR)/css/pact.css).css/' $@
else
	sed -i 's/pact.js/pact.$(shell $(MD5_CMD) $(BUILD_DIR)/js/pact.js).js/' $@
	sed -i 's/pact.css/pact.$(shell $(MD5_CMD) $(BUILD_DIR)/css/pact.css).css/' $@
endif

# Helper things
clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR)

%/.d:
	mkdir -p $(@D)
	touch $@

.PRECIOUS: $(JS_BUILD_DIR)/.d \
	$(CSS_BUILD_DIR)/.d \
	$(DIST_DIR)/.d \
	$(FONTS_DIR)/.d \
	$(JS_DIST_DIR)/.d \
	$(CSS_DIST_DIR)/.d
