from pathlib import Path
import pkgutil
from fastapi import FastAPI
from pydantic import BaseModel
import importlib

PLUGIN_PATH = Path(__file__).parent.joinpath("plugins")

def _plugin_loader() -> list:
    plugins = []
    for _, p, _ in pkgutil.iter_modules([str(PLUGIN_PATH)]):
        plugin = f"plugins.{p}"
        plugins.append(plugin)
    return plugins

plugins = _plugin_loader()
print(plugins)

app = FastAPI()

_plugin_info = {}
_homepage = []
_navbar = {}
for plugin in plugins:
    _plugin_info[plugin] = {
        "endpoints": {},
        "dependencies": []
    }
if plugins:
    _plugins = []
    for plugin in plugins:
        try:
            _plugins.append(importlib.import_module(plugin).Plugin())
        except(AttributeError):
            print(plugin, "seems to be missing required Plugin class")
else:
    print("No Plugins found :(")

print("Starting up")
print("="*25)
print("Loading plugins...")
for plugin in _plugins:
    dependencies = True
    if plugin.dependencies:
        for dependency in plugin.dependencies:
            _plugin_info[plugin.name]["dependencies"].append(dependency)
            if dependency not in _plugin_info.keys():
                print("Dependency", dependency, "not found, not registering endpoints for", plugin.name)
                dependencies = False
    if plugin.endpoints:
        print(plugin.endpoints)
        for endpoint in plugin.endpoints:
            if endpoint["tag"] not in _plugin_info[plugin.name]["endpoints"]:
                _plugin_info[plugin.name]["endpoints"][endpoint["tag"]] = []
            _plugin_info[plugin.name]["endpoints"][endpoint["tag"]].append(endpoint["uri"])
            if endpoint["tag"] == "homepage":
                _homepage.append(endpoint)
            elif endpoint["tag"] == "navbar":
                if plugin.name not in _navbar.keys():
                    _navbar[plugin.name] = []
                _navbar[plugin.name].append(endpoint)


    plugin_register = plugin.register()
    if plugin_register and not dependencies == False:
        app.include_router(plugin_register)

print(_navbar)

@app.get("/")
def root():
    return {"message": "CryptICS"}

@app.get("/plugins", response_model=dict)
def plugins():
    return _plugin_info

@app.get("/plugins/homepage", response_model=list)
def homepage():
    return _homepage

@app.get("/plugins/navbar/{plugin}")
def navbar(plugin: str):
    print(plugin)
    return _navbar["plugins."+plugin]
                
        