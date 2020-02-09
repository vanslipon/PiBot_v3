# PiBot_v3

A robot project :)

## Installation

- sudo apt-get install libportaudio-dev
- curl get.pimoroni.com/skywriter | bash
- sudo apt-get install flac
- pip3 install PyAudio
- sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
- pip3 install SpeechRecognition
- sudo apt-get install mpg321

## References Used

- https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py

## Gyro Calibration

To have more precise gyro angles, `GYRO_MULTIPLIER` has to be appliacted.  
Therefore, let the robot turn for 360° (without calibration), then measure the angle turned, e.g. 380°.  
Now divide 380° by 360° to get the `GYRO_MULTIPLIER` value.  