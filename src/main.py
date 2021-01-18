#!/usr/bin/python3
"""
    Application to measure phone or tablet angle with accelerometer
        Olivier Boesch © 2020
"""
from math import sqrt, acos, pi
from time import sleep
from numbers import Number
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
import plyer

__version__ = '1.0'


class Vector3d:
    def __init__(self, v):
        self.x, self.y, self.z = v[:3]

    @property
    def norm(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __mul__(self, other):
        """redefine self * other as dot product"""
        if isinstance(other, Vector3d):
            return self.x * other.x + self.y * other.y + self.z * other.z
        if isinstance(other, Number):
            return Vector3d((self.x * other, self.y * other, self.z * other))
        raise TypeError


class MecaAccelApp(App):
    event = None
    sensor_on = False
    zero_ref = Vector3d((0, 0, 1))

    def enable_accel(self, on):
        if on:
            self.root.ids['zero_btn'].disabled = False
            self.root.ids['reset_zero_btn'].disabled = False
            self.sensor_on = True
            plyer.accelerometer.enable()
            self.event = Clock.schedule_interval(lambda dt: self.show_angle(), 0.1)
        else:
            self.root.ids['zero_btn'].disabled = True
            self.root.ids['reset_zero_btn'].disabled = True
            self.sensor_on = False
            self.event.cancel()
            plyer.accelerometer.disable()
            self.root.ids['display'].text = "Off"

    def set_zero(self):
        self.zero_ref = Vector3d(plyer.accelerometer.acceleration)
        # give time to do things
        sleep(0.05)

    def reset_zero(self):
        self.zero_ref = Vector3d((0, 0, 1))

    def show_angle(self):
        try:
            v_acceleration = Vector3d(plyer.accelerometer.acceleration)
            # compute angle
            cosang = (v_acceleration * self.zero_ref) / (v_acceleration.norm * self.zero_ref.norm)
            Logger.debug("Angle: {:f}".format(cosang))
            ang = acos(cosang) * 180 / pi
            self.root.ids['display'].text = "{:.0f}°".format(ang)
        except TypeError:  # if None is output
            pass


if __name__ == '__main__':
    app = MecaAccelApp()
    app.run()
