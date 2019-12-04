"""Plugin initialization module

Qgis automatically calls an installed plugin's :py:func:`classFactory` to
actually load the plugin.

Note: beforehand we call our dependency mechanism (see
:doc:`linked_external-dependencies_readme`) to ensure all dependencies are
there.

"""
from pathlib import Path
from ThreeDiToolbox import dependencies

import faulthandler
import sys


#: Handy constant for building relative paths.
PLUGIN_DIR = Path(__file__).parent


# sys.stderr is not available under Windows in Qgis, which is what the faulthandler
# uses by default.
if sys.stderr is not None:
    faulthandler.enable()
dependencies.ensure_everything_installed()


from ThreeDiToolbox.utils.my_widgets import MyCustomWidgetFactory
from qgis.gui import QgsGui

widget_editor_registry = QgsGui.editorWidgetRegistry()
widget_editor_registry.registerWidget(
    widgetId='mywidget',
    widgetFactory=MyCustomWidgetFactory(name='mywidget123')
)


def classFactory(iface):
    """Return ThreeDiToolbox class from file ThreeDiToolbox.

    In addition, we set up python logging (see
    :py:mod:`ThreeDiToolbox.utils.qlogging`).

    args:
        iface (QgsInterface): A QGIS interface instance.

    """
    from ThreeDiToolbox.utils.qlogging import setup_logging

    import sys; sys.path[0:0] = ['/pycharm/pydevd-pycharm.egg', ]; import pydevd; pydevd.settrace('10.90.16.34', port=4445, stdoutToServer=True, stderrToServer=True, suspend=False)


    setup_logging()
    dependencies.check_importability()

    from .threedi_plugin import ThreeDiPlugin

    return ThreeDiPlugin(iface)
