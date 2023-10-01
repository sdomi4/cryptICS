from core import ExpCryptBackend
from pathlib import Path
import pkgutil
from fastapi import FastAPI

PLUGIN_PATH = Path(__file__).parent.joinpath("plugins")

def _plugin_loader() -> list:
    plugins = []
    for _, p, _ in pkgutil.iter_modules([str(PLUGIN_PATH)]):
        plugin = f"plugins.{p}"
        plugins.append(plugin)
    return plugins

plugins = _plugin_loader()
print(plugins)

for plugin in plugins:
    # check if all plugin dependencies are loaded
    pass

app = FastAPI()
app = ExpCryptBackend(app, plugins)
app = app.run()


@app.get("/")
def root():
    return {"message": "CryptICS"}

@app.get("/plugins", response_model=list)
def plugins():
    return plugins