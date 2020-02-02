import math
import time

from bot.movement import motor_controls as mc
from bot import gyro_movement as gm
from bot.sensing import ultrasonic as us

if __name__ == "__main__":

    motor_speed = 75
    mc.change_speed_right(motor_speed)
    mc.change_speed_left(motor_speed)
    gyro_z_sensor_drift = gm.get_gyro_z_sensor_drift()

    while True:
        try:
            dist = us.get_distance()
            if dist < 20:
                mc.say_no()
                gm.gyro_turn(50, False, gyro_z_sensor_drift)
            else:
                mc.move_front()
            time.sleep(0.1)
        except KeyboardInterrupt:
            break