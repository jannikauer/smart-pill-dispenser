# smart-pill-dispenser

The smart_pill_dispenser project was implemented as part of university course about hardware related software development. The idea was to create a device, that helps patients with dementia to take the right doses of their medication at the right time. The prototype can be seen in the image below:



The following youtube video demonstrates the usecase :
[smart-pill-dispenser pitch](https://www.youtube.com/watch?v=3C0Cy7S0aK0)

## User scenario
The patient brings their smart-pill-dispenser to the doctor, who then uploads the prescribed medicine onto the device via a webserver. At the patients home a caregiver can then fill up the device with the right medication after activating the "filling" mode, where the doses and types of medication are shown on the display. After that the "weekly use" mode can be activated and the device will then remind the patient to take the medication and dispense the correct pills.



## Implementation
The device was implemented with a TTGO Lillygo ESP32 Microcontroller and the code was written with MicroPython. The hardware was designed in Autodesk inventor and then 3d printed

- Use TTGO Lillygo with correct firmware (Github Repo Link: https://github.com/russhughes/st7789_mpy)
- Upload Main.py to ESP32 (Lillygo)
- Open Webrepl.html
- Connect to ESP32 via Wi-Fi
- Upload Medikamente.txt
- Password = 12345678
- Lillygo ready with current medication set


