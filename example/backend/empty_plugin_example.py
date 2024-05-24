###########################################
#   Example for a new plugin with needed  #
#   class / methods for plugin discovery  #
###########################################

# To export API endpoints
from fastapi import APIRouter

# All logic should be contained in the Plugin class, for plugin discovery/import
class Plugin():

    # Plugin metadata
    name = "plugins.example"
    # Full names (e.g. "plugins.diff") of all dependencies in a list
    dependencies = []
    # API endpoints contained in the plugin
    # should contain the URI and relevant tags so they can be discovered / loaded by the frontend
    # tags determine where the URLs might be loaded in the frontend
    #
    # predefined tags:
    # - homepage: the starting point, dynamically added to the front page (with the extra field "description" for the text on the home page)
    #
    # there are currently no forther uses for tags, but that would allow additional logic if needed
    endpoints = [
        {
            "uri": "/example",
            "tag": "homepage",
            "description": {
                "de": "Beispiel",
                "en": "Example"
            }
        }
    ]

    # Instantiate router instance, all plugins are prefixed with at least /plugins
    router = APIRouter(
        prefix="/plugins"
    )

    # method called during plugin discovery to register API endpoints
    # return None if no endpoints should be registered
    def register(self):
        # return None
        return self.router
    
    # Add any API endpoints and logic methods as needed for the plugin
    @router.get("/example", response_model=[])
    def run():
        # do things
        return {"message": "example"}
    
    @router.post("/example", response_model=[])
    def run():
        # do things
        return {"message": "example"}