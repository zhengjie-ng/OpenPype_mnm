# -*- coding: utf-8 -*-
"""Collect scene data."""
import os

import pyblish.api
from avalon import harmony


class CollectScene(pyblish.api.ContextPlugin):
    """Collect basic scene information."""

    label = "Scene Data"
    order = pyblish.api.CollectorOrder
    hosts = ["harmony"]

    def process(self, context):

        sig = harmony.signature()
        func = """function %s()
        {
            return [
                about.getApplicationPath(),
                scene.currentProjectPath(),
                scene.currentScene(),
                scene.getFrameRate(),
                scene.getStartFrame(),
                scene.getStopFrame(),
                sound.getSoundtrackAll().path(),
                scene.defaultResolutionX(),
                scene.defaultResolutionY()
            ]
        }
        %s
        """ % (sig, sig)
        result = harmony.send(
            {"function": func, "args": []}
        )["result"]

        context.data["applicationPath"] = result[0]
        context.data["scenePath"] = os.path.join(
            result[1], result[2] + ".xstage")
        context.data["frameRate"] = result[3]
        context.data["frameStart"] = result[4]
        context.data["frameEnd"] = result[5]
        context.data["audioPath"] = result[6]
        context.data["resolutionWidth"] = result[7]
        context.data["resolutionHeight"] = result[8]

        all_nodes = harmony.send(
            {"function": "node.subNodes", "args": ["Top"]}
        )["result"]

        context.data["all_nodes"] = all_nodes
