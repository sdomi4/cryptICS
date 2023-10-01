import importlib
from fastapi import FastAPI


class ExpCryptBackend():
    def __init__(self, app, plugins:list=[]):
        self.app = app
        self._plugin_list = plugins
        if plugins:
            self._plugins = [
                importlib.import_module(plugin).Plugin() for plugin in plugins
            ]
        else:
            print("No Plugins found :(")

    def run(self):
        print("Starting up")
        print("="*25)
        print("Loading plugins...")
        for plugin in self._plugins:
            dependencies = True
            plugin_dependencies = plugin.dependencies()
            if plugin_dependencies:
                for dependency in plugin_dependencies:
                    if dependency not in self._plugin_list:
                        print("Dependency", dependency, "not found, not registering endpoints for", plugin)
                        dependencies = False
            plugin_register = plugin.register()
            if plugin_register and not dependencies == False:
                self.app.include_router(plugin_register)
        return self.app