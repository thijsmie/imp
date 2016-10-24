#import application
#import models
#import response
#import security

from pluginbase import PluginBase


plugin_base = PluginBase(package='imp.plugins')
plugin_src  = plugin_base.make_plugin_source(searchpath=["./plugins"])

#plugin_src.appdata = {"app": application, "models": models, "response": response, "security": security}

plugins = []
for plugin in plugin_src.list_plugins():
    plugins.append(plugin_src.load_plugin(plugin))

