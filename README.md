# Smart Pill Dispenser

The Smart Pill Dispenser project was developed as part of a university course focusing on hardware-related software development. The aim was to create a device that assists patients with dementia in taking the correct doses of their medication at the appropriate times. The prototype can be seen in the image below, as well as in a short pitch video available on YouTube:

<img src="https://github.com/jannikauer/smart-pill-dispenser/blob/main/smart-pill-dispenser.jpg" alt="smart-pill-dispenser image" width="300">

[Watch the Smart Pill Dispenser Pitch Video](https://www.youtube.com/watch?v=3C0Cy7S0aK0)

## User Scenario

The patient brings their Smart Pill Dispenser to the doctor, who then uploads the prescribed medication onto the device via a web server. Once back at home, a caregiver can fill the device with the correct medication after activating the "filling" mode. During this mode, the doses and types of medication are displayed on the device's screen. Afterward, the "weekly use" mode can be activated, prompting the device to remind the patient to take their medication while dispensing the correct pills at the designated times of the day.

## Implementation

The device was built using a TTGO Lillygo ESP32 microcontroller, and the code was written in MicroPython. The hardware design was created using Autodesk Inventor and then 3D printed.

### Getting Started

To set up the Smart Pill Dispenser, follow these steps:

1. Use TTGO Lillygo with the correct firmware. You can find the firmware on [GitHub](https://github.com/russhughes/st7789_mpy).
2. Upload `Main.py` to the ESP32 (Lillygo).
3. Open `Webrepl.html`.
4. Connect to the ESP32 via Wi-Fi.
5. Upload `medication.txt`.
6. Enter the password (default: 12345678).
7. Your Lillygo device is now ready with the current medication set.

