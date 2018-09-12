import ac
from math import sin, cos, pi
from app.ac_lib import GL, Color, Point, ACCAR, ACLAP


class ACObject(object):
    def __init__(self, type, app):
        self.ac_obj = 0
        self._pos = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._text = ""
        self._font_size = 10
        self._font_ratio = 0.5
        self._font_color = Color(1, 1, 1, 1)
        self._background_texture = 0
        self._background = False
        self._background_color = Color(0, 0, 0, 0)
        self._border = False
        self._border_color = Color(1, 1, 1, 1)

        if self.ac_obj is not None:
            ac.setPosition(self.ac_obj, self._pos[0], self._pos[1])

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        _x, _y = pos
        if isinstance(_x, int) and isinstance(_y, int):
            self._pos = (_x, _y)

            if self.ac_obj != 0:
                ac.setPosition(self.ac_obj, _x, _y)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        _w, _h = size
        if isinstance(_w, int) and isinstance(_h, int):
            self._font_size = min(self.getFontSizeFromText(), _h)
            self._size = (_w, _h)

            if self.ac_obj != 0:
                ac.setFontSize(self.ac_obj, self._font_size)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible

            if self.ac_obj != 0:
                ac.setVisible(visible)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        if isinstance(font_size, int):
            self._font_size = min(int(font_size), self._size[1])

            if self.ac_obj != 0:
                ac.setFontSize(self.ac_obj, self._font_size)

    @property
    def font_ratio(self):
        return self._font_ratio

    @font_ratio.setter
    def font_ratio(self, font_ratio):
        if isinstance(font_ratio, int):
            self._font_ratio = min(int(font_ratio), self._size[1])

            if self.ac_obj != 0:
                ac.setFontSize(self.ac_obj, self._font_size)

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, font_color):
        if isinstance(font_color, Color):
            self._font_color = font_color

            if self.ac_obj != 0:
                ac.setFontColor(self.ac_obj, self._font_color.r, self._font_color.g, self._font_color.b, self._font_color.a)

    @property
    def background_texture(self):
        return self._background_texture

    @background_texture.setter
    def background_texture(self, tex):
        if isinstance(tex, str):
            self._background_texture = ac.newTexture(tex)
        else:
            self._background_texture = tex

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        if isinstance(background_color, Color):
            self._background_color = background_color

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, border):
        if isinstance(border, bool):
            self._border = border

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        if isinstance(border_color, Color):
            self._border_color = border_color

    def setRenderCallback(self, callback):
        if self.ac_obj != 0:
            ac.addRenderCallback(self.ac_obj, callback)

    def setText(self, text):
        self._text = text
        if self.ac_obj != 0:
            ac.setText(self.ac_obj, text)

    def setTextAlignment(self, alignment="center"):
        if self.ac_obj != 0:
            if alignment == "left":
                ac.setPosition(self.ac_obj, self.pos[0], self.pos[1])
            elif alignment == "center":
                ac.setPosition(self.ac_obj, int(self.pos[0] + self.size[0] / 2), self.pos[1])
            elif alignment == "right":
                ac.setPosition(self.ac_obj, int(self.pos[0] + self.size[0]), self.pos[1])
            ac.setFontAlignment(self.ac_obj, alignment)

    '''
    # Calculates and returns the text width either of the given text or the saved
    # text in the object
    '''

    def getTextWidth(self, text):
        if text != "":
            return len(text) * (self._font_size * self._font_ratio)
        else:
            return len(self._text) * (self._font_size * self._font_ratio)

    '''
    # Calculates and returns the ideal font size depending on the maximum width of the object
    '''

    def getFontSizeFromText(self):
        return self._size[0] / max(1, len(self._text)) * (1 + self._font_ratio)

    '''
    # shows the object
    '''

    def show(self):
        if self.ac_obj != 0:
            ac.setVisible(self.ac_obj, True)

    '''
    # hides the object
    '''

    def hide(self):
        if self.ac_obj != 0:
            ac.setVisible(self.ac_obj, False)


class App:
    def __init__(self, app_name, x, y, w, h):
        self.children = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.app = ac.newApp(app_name)
        ac.setTitle(self.app, app_name)
        ac.setPosition(self.app, self.x, self.y)
        ac.setSize(self.app, self.w, self.h)
        ac.setIconPosition(self.app, 0, -10000)
        ac.setTitlePosition(self.app, 0, -10000)
        ac.drawBorder(self.app, 0)
        ac.drawBackground(self.app, 0)

        self.update()

    def update(self):
        ac.setBackgroundColor(self.app, 0, 0, 0)
        ac.setBackgroundOpacity(self.app, 0)
        # for child in self.children:
        #     child.update()

    def render(self):
        for child in self.children:
            child.render()


class Speedometer:
    def __init__(self, app, w, h):
        self.w = w
        self.h = h
        self.x_offset = 20
        self.y_offset = 140
        self.shift_progress = 0
        self.shift_color = 0
        self.tyre_color = [Color(0, 0.7, 0, 1)] * 4
        self.brake_color = [Color(0, 0.7, 0, 1)] * 4

        self.green = Color(0.0, 0.7, 0, 1)
        self.lime = Color(0.3, 0.5, 0.1, 1)
        self.yellow = Color(0.7, 0.7, 0, 1)
        self.orange = Color(1, 0.7, 0, 1)
        self.red = Color(0.8, 0, 0, 1)
        self.blue = Color(0.1, 0.5, 0.8, 1)

        self.gear = ac.addLabel(app, "")
        ac.setPosition(self.gear, self.x_offset + 80, self.y_offset - 100)
        ac.setFontSize(self.gear, 100)

        self.tyre_FL = ac.addLabel(app, "")
        ac.setFontSize(self.tyre_FL, 10)
        self.tyre_FR = ac.addLabel(app, "")
        self.tyre_RL = ac.addLabel(app, "")
        self.tyre_RR = ac.addLabel(app, "")

        self.speed = ac.addLabel(app, "")
        ac.setPosition(self.speed, self.x_offset + 150, self.y_offset)
        ac.setFontSize(self.speed, 60)
        ac.setFontAlignment(self.speed, "right")

        self.speed_unit_top = ac.addLabel(app, "")
        ac.setPosition(self.speed_unit_top, self.x_offset + 160, self.y_offset + 10)
        ac.setFontSize(self.speed_unit_top, 30)
        ac.setFontColor(self.speed_unit_top, 0.1, 0.5, 0.8, 1)

        self.speed_unit_bot = ac.addLabel(app, "")
        ac.setPosition(self.speed_unit_bot, self.x_offset + 170, self.y_offset + 40)
        ac.setFontSize(self.speed_unit_bot, 30)
        ac.setFontColor(self.speed_unit_bot, 0.1, 0.5, 0.8, 1)

        self.rpm = ac.addLabel(app, "")
        ac.setPosition(self.rpm, self.x_offset + 150, self.y_offset + 70)
        ac.setFontSize(self.rpm, 30)
        ac.setFontAlignment(self.rpm, "right")

        self.rpm_unit = ac.addLabel(app, "")
        ac.setPosition(self.rpm_unit, self.x_offset + 150, self.y_offset + 70)
        ac.setFontSize(self.rpm_unit, 30)
        ac.setFontColor(self.rpm_unit, 0.1, 0.5, 0.8, 1)

        self.best_lap = ac.addLabel(app, "")
        ac.setPosition(self.best_lap, self.x_offset + 380, self.y_offset - 90)
        ac.setFontSize(self.best_lap, 30)
        ac.setFontAlignment(self.best_lap, "right")
        ac.setFontColor(self.best_lap, 0, 0.7, 0, 1)

        self.last_lap = ac.addLabel(app, "")
        ac.setPosition(self.last_lap, self.x_offset + 380, self.y_offset - 60)
        ac.setFontSize(self.last_lap, 30)
        ac.setFontAlignment(self.last_lap, "right")

        self.current_lap = ac.addLabel(app, "")
        ac.setPosition(self.current_lap, self.x_offset + 380, self.y_offset - 30)
        ac.setFontSize(self.current_lap, 30)
        ac.setFontAlignment(self.current_lap, "right")

        self.delta_lap = ac.addLabel(app, "")
        ac.setPosition(self.delta_lap, self.x_offset + 380, self.y_offset)
        ac.setFontSize(self.delta_lap, 30)
        ac.setFontAlignment(self.delta_lap, "right")

        self.prev_car = ac.addLabel(app, "")
        ac.setPosition(self.prev_car, self.x_offset + 400, self.y_offset + 60)
        ac.setFontSize(self.prev_car, 30)
        ac.setFontAlignment(self.prev_car, "right")
        ac.setFontColor(self.prev_car, 0.7, 0, 0, 1)

        self.next_car = ac.addLabel(app, "")
        ac.setPosition(self.next_car, self.x_offset + 400, self.y_offset + 90)
        ac.setFontSize(self.next_car, 30)
        ac.setFontAlignment(self.next_car, "right")
        ac.setFontColor(self.next_car, 0, 0.7, 0, 1)

        self.update()

    def update(self):

        ac.setText(self.gear, "{0}".format(ACCAR.getGear()))
        ac.setText(self.speed, "{0:.0f}".format(ACCAR.getSpeed()))
        ac.setText(self.speed_unit_top, "km")
        ac.setText(self.speed_unit_bot, "h")
        ac.setText(self.rpm, "{0:.0f}".format(ACCAR.getRPM()))
        ac.setText(self.rpm_unit, "rpm")
        ac.setText(self.best_lap, "B: {0}".format(ACLAP.getBestLap()))
        ac.setText(self.last_lap, "L: {0}".format(ACLAP.getLastLap()))
        ac.setText(self.current_lap, "C: {0}".format(ACLAP.getCurrentLap()))
        ac.setText(self.delta_lap, "D: {0}".format(ACLAP.getLapDelta()))
        ac.setText(self.prev_car, "P: {0}".format(ACCAR.getPrevCarDiff()))
        ac.setText(self.next_car, "N: {0}".format(ACCAR.getNextCarDiff()))

        # Tyres
        for i in range(0, 4):
            tyre_wear = ACCAR.getTyreWear(i)
            if tyre_wear > 90:
                self.tyre_color[i] = self.green
            elif 90 > tyre_wear > 80:
                self.tyre_color[i] = self.lime
            elif 80 > tyre_wear > 70:
                self.tyre_color[i] = self.yellow
            elif 70 > tyre_wear > 60:
                self.tyre_color[i] = self.orange
            elif 60 > tyre_wear > 50:
                self.tyre_color[i] = self.red

        for i in range(0, 4):
            brake_temp = ACCAR.getBrakeTemperature(i)
            if brake_temp > 90:
                self.brake_color[i] = self.green
            elif 90 > brake_temp > 80:
                self.brake_color[i] = self.lime
            elif 80 > brake_temp > 70:
                self.brake_color[i] = self.yellow
            elif 70 > brake_temp > 60:
                self.brake_color[i] = self.orange
            elif 60 > brake_temp > 50:
                self.brake_color[i] = self.red

        # Shifting
        self.shift_progress = ACCAR.getRPM() / ACCAR.getRPMMax()

        if 0 <= self.shift_progress <= 0.3:
            self.shift_color = self.green
            ac.setFontColor(self.rpm, 0, 0.7, 0, 1)
        elif 0.3 < self.shift_progress <= 0.6:
            self.shift_color = self.lime
            ac.setFontColor(self.rpm, 0.3, 0.5, 0.1, 1)
        elif 0.6 < self.shift_progress <= 0.8:
            self.shift_color = self.yellow
            ac.setFontColor(self.rpm, 1, 0.8, 0, 1)
        elif 0.8 < self.shift_progress <= 0.95:
            self.shift_color = self.orange
            ac.setFontColor(self.rpm, 1, 0.7, 0, 1)
        elif self.shift_progress > 0.95:
            self.shift_color = self.red
            ac.setFontColor(self.rpm, 0.8, 0, 0, 1)

    def render(self):
        # Gear __ Speed separator
        GL.rect(self.x_offset + 80, self.y_offset + 15, 120, 4)

        # Tyres
        GL.rect(self.x_offset + 150, self.y_offset - 65, 20, 30, self.tyre_color[0])
        GL.rect(self.x_offset + 150, self.y_offset - 65, 20, 30, filled=False)
        GL.rect(self.x_offset + 165, self.y_offset - 60, 10, 20, self.brake_color[0])
        GL.rect(self.x_offset + 165, self.y_offset - 60, 10, 20, filled=False)

        GL.rect(self.x_offset + 190, self.y_offset - 65, 20, 30, self.brake_color[1])
        GL.rect(self.x_offset + 190, self.y_offset - 65, 20, 30, filled=False)
        GL.rect(self.x_offset + 185, self.y_offset - 60, 10, 20, self.tyre_color[1])
        GL.rect(self.x_offset + 185, self.y_offset - 60, 10, 20, filled=False)

        GL.rect(self.x_offset + 150, self.y_offset - 30, 20, 30, self.brake_color[2])
        GL.rect(self.x_offset + 150, self.y_offset - 30, 20, 30, filled=False)
        GL.rect(self.x_offset + 165, self.y_offset - 25, 10, 20, self.tyre_color[2])
        GL.rect(self.x_offset + 165, self.y_offset - 25, 10, 20, filled=False)

        GL.rect(self.x_offset + 190, self.y_offset - 30, 20, 30, self.brake_color[3])
        GL.rect(self.x_offset + 190, self.y_offset - 30, 20, 30, filled=False)
        GL.rect(self.x_offset + 185, self.y_offset - 25, 10, 20, self.tyre_color[3])
        GL.rect(self.x_offset + 185, self.y_offset - 25, 10, 20, filled=False)

        # Speed Unit Separator ___
        GL.rect(self.x_offset + 160, self.y_offset + 45, 45, 3)

        # Speed Indicator
        radius_outter = 240
        radius_inner = 220
        rad = 1.5 * pi
        rad_step = 1.5 * pi / 2 * pi / 360
        step = 0
        c_x = self.x_offset + 220
        c_y = self.y_offset + 100

        while rad < 2 * pi:
            if step % 10 >= 8:
                GL.line(c_x + (sin(rad) * radius_outter), c_y - (cos(rad) * radius_outter),
                        c_x + (sin(rad) * radius_inner), c_y - (cos(rad) * radius_inner), self.blue)
            else:
                GL.line(c_x + (sin(rad) * radius_outter), c_y - (cos(rad) * radius_outter),
                        c_x + (sin(rad) * radius_inner), c_y - (cos(rad) * radius_inner))

            rad_progress = (rad - 1.5 * pi) / (0.5 * pi)
            if self.shift_progress >= rad_progress:
                GL.line(c_x + (sin(rad) * radius_outter), c_y - (cos(rad) * radius_outter),
                        c_x + (sin(rad) * radius_inner), c_y - (cos(rad) * radius_inner), self.shift_color)
            rad += rad_step
            step += 1
        
        # Lap Progress
        lap_progress = ACCAR.getLocation()
        GL.rect(self.x_offset - 20, self.y_offset + 110, lap_progress * radius_outter, 6, self.blue)
        GL.line(self.x_offset - 20, self.y_offset + 110, self.x_offset - 20, self.y_offset + 120)
        GL.line(self.x_offset + radius_inner, self.y_offset + 110, self.x_offset + radius_inner, self.y_offset + 120)
