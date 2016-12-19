#!/usr/bin/env python3
import os
import sys

OUTPUT_FORMAT = """
angular.module('{module}').run(["$templateCache", function($templateCache) {{
    $templateCache.put("{template_name}",
        "{template}");
}}]);
"""


def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    _, source_file, module, target_file = sys.argv
    template_name = source_file.split('src/')[1]
    try:
        os.makedirs(os.path.dirname(target_file))
    except OSError:
        pass
    if os.path.exists(target_file):
        os.unlink(target_file)
    with open(target_file, 'w', encoding="utf-8") as target:
        with open(source_file, 'r', encoding="utf-8") as source:
            target.write(
                OUTPUT_FORMAT.format(
                    template=source.read().replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n" + \n"'),
                    module=module,
                    template_name=template_name
                )
            )


if __name__ == '__main__':
    main()
