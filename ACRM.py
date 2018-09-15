import ac
import acrm.ac_gui as gui
import acrm.ac_lib as lib


def acMain(ac_version):
    global app_speedometer, speedometer

    app_name = "ACRM"
    x = 200
    y = 200
    w = 450
    h = 300

    # Speedometer
    app_speedometer = gui.App(app_name, x, y, w, h)
    speedometer = gui.Speedometer(app_speedometer.app, w, h)

    app_speedometer.children.append(speedometer)

    ac.addRenderCallback(app_speedometer.app, glRender)

    return app_name


def acUpdate(delta):
    global app_speedometer, speedometer

    app_speedometer.update()
    speedometer.update()


def glRender(delta):
    global app_speedometer, speedometer

    app_speedometer.render()
    speedometer.render()


def acShutdown():
    i = 1
