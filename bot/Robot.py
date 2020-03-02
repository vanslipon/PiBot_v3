import time
from multiprocessing.pool import ThreadPool
import RPi.GPIO as GPIO
from threading import Thread
import os
from datetime import datetime

from movement import powertrain
from sensing import mpu6050, hcsr04, microphone, speaker, camera
from combination import gyro_movement

GPIO.setmode(GPIO.BCM)


class Robot():

    motor_speed_left = 75
    motor_speed_right = 75
    gyro_z_sensor_drift = -1.8
    is_driving = False

    ultrasonic = None
    powertrain = None
    gyro_accel = None
    microphone = None

    def __init__(self, ultrasonic, powertrain, gyro_accel, microphone, speaker, camera):
        self.ultrasonic = ultrasonic
        self.powertrain = powertrain
        self.gyro_accel = gyro_accel
        self.microphone = microphone
        self.speaker = speaker
        self.camera = camera

        self.is_driving = False

        self.gyro_z_sensor_drift = self.gyro_accel.get_gyro_z_sensor_drift()

    def start(self):
        self.speaker.say_hi()
        while True:
            spoken_words = self.microphone.recognize_speech().lower()
            print('I understood:', spoken_words)
            if any(ext in spoken_words for ext in ['left']):
                print('Turning left.')
                self.gyro_turn(90, False)
            elif any(ext in spoken_words for ext in ['right']):
                print('Turning right.')
                self.gyro_turn(90, True)
            elif any(ext in spoken_words for ext in ['forward', 'front', 'go', 'drive']):
                print('Moving forward.')
                self.powertrain.move_front()
                time.sleep(3)
                self.powertrain.stop_motors()
            elif any(ext in spoken_words for ext in ['backward', 'back']):
                print('Moving backward.')
                self.powertrain.move_back()
                time.sleep(3)
                self.powertrain.stop_motors()
            elif any(ext in spoken_words for ext in ['auto', 'autonomous']):
                print('Started autonomous driving mode.')
                self.drive_around()
            elif any(ext in spoken_words for ext in ['around']):
                print('Turning around.')
                self.gyro_turn(180, True)
            else:
                print('No recognized command! ->', spoken_words)

    def turn_look_for_object(self, gyro_movement, object_name):
        for _ in range(6):
            x_diff, box_img_ratio = self.camera.look_for_object(object_name)
            if x_diff != 0:
                return x_diff, box_img_ratio
            gyro_movement.gyro_turn(60, motor_speed=100)
        return 0, 0

    def test(self):

        gm = gyro_movement.gyro_movement(self.powertrain, self.gyro_accel)

        search_object = 'person'
        self.motor_speed_left = 60
        self.motor_speed_right = 60

        x_diff, box_img_ratio = self.turn_look_for_object(gm, search_object)
        while True:
            if (abs(x_diff)) > 10:
                right = True if x_diff < 0 else False
                gm.gyro_turn(abs(x_diff), right)
                x_diff, box_img_ratio = self.turn_look_for_object(gm, search_object)
                if x_diff == 0 and box_img_ratio == 0:
                    print('Lost object!')
                    break
            else:
                if box_img_ratio < 0.5:
                    self.motor_speed_left = 90
                    self.motor_speed_right = 90
                    gm.gyro_move_start(True)
                    time.sleep(1)
                    gm.gyro_move_stop()
                    self.motor_speed_left = 60
                    self.motor_speed_right = 60
                time.sleep(0.5)
                x_diff, box_img_ratio = self.turn_look_for_object(gm, search_object)

    def _test(self):
        self.camera.take_picture(str(datetime.now()) + '.jpg')


# ultrasonic
US_TRIGGER_PIN = 17
US_ECHO_PIN = 4

# powertrain
POWERTRAIN_IN1_PIN = 19
POWERTRAIN_IN2_PIN = 13
POWERTRAIN_IN3_PIN = 6
POWERTRAIN_IN4_PIN = 5
POWERTRAIN_ENA_PIN = 26
POWERTRAIN_ENB_PIN = 11
MOTORSPEED_LEFT = 75
MOTORSPEED_RIGHT = 75


us = hcsr04.hcsr04(US_TRIGGER_PIN, US_ECHO_PIN)

pt = powertrain.powertrain(
    POWERTRAIN_IN1_PIN,
    POWERTRAIN_IN2_PIN,
    POWERTRAIN_IN3_PIN,
    POWERTRAIN_IN4_PIN,
    POWERTRAIN_ENA_PIN,
    POWERTRAIN_ENB_PIN,
    MOTORSPEED_LEFT,
    MOTORSPEED_RIGHT)

mpu = mpu6050.mpu6050(0x68)
mic = microphone.microphone()
speaker = speaker.speaker()
camera = camera.camera()

robot = Robot(us, pt, mpu, mic, speaker, camera)
robot.test()
