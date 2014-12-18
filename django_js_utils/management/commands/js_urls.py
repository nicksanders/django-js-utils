from __future__ import print_function

import json
import sys
import re
from types import ModuleType

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.core.management.base import BaseCommand
from django.utils.datastructures import SortedDict
from django.conf import settings


RE_KWARG = re.compile(r"(\(\?P\<(.*?)\>.*?\))")  # Pattern for named parameters in urls
RE_ARG = re.compile(r"(\(.*?\))")  # Pattern for recognizing unnamed url parameters


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create urls.js file by parsing all of the urlpatterns in the root urls.py file
        """
        try:
            URLS_JS_GENERATED_FILE = getattr(settings, 'URLS_JS_GENERATED_FILE')
        except:
            raise ImproperlyConfigured('You should provide URLS_JS_GENERATED_FILE setting.')

        js_patterns = SortedDict()

        verbosity = int(options['verbosity'])
        if verbosity > 0:
            print("Generating Javascript urls file %s" % URLS_JS_GENERATED_FILE)

        Command.handle_url_module(
            js_patterns, settings.ROOT_URLCONF, verbosity=verbosity)

        #output to the file
        urls_file = open(URLS_JS_GENERATED_FILE, "w")
        urls_file.write("dutils.conf.urls = ")
        json.dump(js_patterns, urls_file)
        urls_file.write(";")
        urls_file.close()

        if verbosity > 0:
            print("Done generating Javascript urls file %s" % URLS_JS_GENERATED_FILE)

    @staticmethod
    def handle_url_module(js_patterns, module_name, prefix="", verbosity=1):
        """
        Load the module and output all of the patterns
        Recurse on the included modules
        """

        URLS_JS_I18N = None
        if hasattr(settings, 'URLS_JS_I18N'):
            URLS_JS_I18N = settings.URLS_JS_I18N

        if isinstance(module_name, str):
            if verbosity > 2:
                print('(str) %s: %s ' % (module_name, prefix))
            __import__(module_name)
            root_urls = sys.modules[module_name]
            patterns = root_urls.urlpatterns

        elif isinstance(module_name, ModuleType) and hasattr(module_name, 'urlpatterns'):
            if verbosity > 2:
                print('(ModuleType) %s: %s' % (module_name, prefix))
            root_urls = module_name
            patterns = root_urls.urlpatterns

        if not 'patterns' in locals():
            if verbosity > 2:
                print('%s: %s' % (module_name, prefix))
            root_urls = module_name
            patterns = root_urls

        try:
            for pattern in patterns:
                if issubclass(pattern.__class__, RegexURLPattern):

                    if not pattern.name:
                        continue

                    key = pattern.name
                    if prefix == '^admin/':
                        key = 'admin:' + key

                    full_url = prefix + pattern.regex.pattern
                    for chr in ["^", "$"]:
                        full_url = full_url.replace(chr, "")

                    # Handle kwargs, args
                    kwarg_matches = RE_KWARG.findall(full_url)
                    if kwarg_matches:
                        for el in kwarg_matches:
                            ## Prepare the output for JS resolver
                            full_url = full_url.replace(el[0], "<%s>" % el[1])

                    #after processing all kwargs try args
                    args_matches = RE_ARG.findall(full_url)
                    if args_matches:
                        for el in args_matches:
                            ## Replace by a empty parameter name
                            full_url = full_url.replace(el, "<>")

                    if URLS_JS_I18N and full_url.startswith('en-us'):
                        full_url = full_url.replace('en-us', '<language_code>')

                    js_patterns[key] = "/" + full_url

                elif issubclass(pattern.__class__, RegexURLResolver):
                    if not pattern.urlconf_name:
                        continue
                    Command.handle_url_module(js_patterns, pattern.urlconf_name,
                                              prefix=prefix + pattern.regex.pattern,
                                              verbosity=verbosity)
        except TypeError:
            print("Couldn't iterate over patterns")
            print(patterns)
