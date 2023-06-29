import pyblish.api

from openpype.pipeline import (
    publish,
    PublishValidationError
)

from openpype.pipeline.colorspace import (
    get_ocio_config_colorspaces
)


class ValidateColorspace(pyblish.api.InstancePlugin,
                         publish.OpenPypePyblishPluginMixin,
                         publish.ColormanagedPyblishPluginMixin):
    """Validate representation colorspaces"""

    label = "Validate representation colorspace"
    order = pyblish.api.ValidatorOrder
    hosts = ["traypublisher"]

    def process(self, instance):

        config_colorspaces = {}  # cache of colorspaces per config path
        for repre in instance.data.get("representations", {}):

            colorspace_data = repre.get("colorspaceData", {})
            if not colorspace_data:
                # Nothing to validate
                continue

            config_path = colorspace_data["config"]["path"]
            if config_path not in config_colorspaces:
                colorspaces = get_ocio_config_colorspaces(config_path)
                config_colorspaces[config_path] = set(colorspaces)

            colorspace = colorspace_data["colorspace"]
            self.log.debug(
                f"Validating representation '{repre['name']}' "
                f"colorspace '{colorspace}'"
            )
            if colorspace not in config_colorspaces[config_path]:
                message = (
                    f"Representation '{repre['name']}' colorspace "
                    f"'{colorspace}' does not exist in OCIO config: "
                    f"{config_path}"
                )

                raise PublishValidationError(
                    title="Representation colorspace",
                    message=message,
                    description=message
                )
