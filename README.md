# HiRISE Demo

## Software Requiremements  

- Raspberry Pi OS Lite (64-bit) - No GUI/Desktop Environment
- Miniforge3 or Anaconda (use conda-forge channel)

### Install Via Apt

- make (optional, but simplifies running)
- libedgetpu-max or libedgetpu-std (for running models on the TPU)
- xorg

## Hardware Requirements

- Raspberry Pi 5
- USB-C Google Coral TPU
- USB Camera (4K recommended)
- Monitor (1920x1080p recommened)
- Keyboard
- Mouse

## Setup Instructions:

1. Install your Raspberry Pi 5 with Raspberry Pi OS Lite 64-bit. Note this OS does not contain a GUI or Desktop Environment. You should be thoroughly familiar with using the linux command line prior to starting.
2. After installing the OS on the Pi 5, you will need to install one of the Coral Edge TPU libraries: libedgetpu-std or libedgetpu-max. We used the max version in our demo for the highest YOLO inference performance.
3. Ensure that you also install xorg (for displaying the demo GUI headlessly) and make (for making running simpler).
4. Install  a conda-forge channel compatible version of conda like [Miniforge3](https://github.com/conda-forge/miniforge?tab=readme-ov-file#install).
5. Create the conda environment specified in the `env.yml` file using `mamba env create -f env.yml` or `conda env create -f env.yml`. We recomment using the `mamba` command since mamba is typically faster at solving dependencies and conflicts.
6. Activate the `hirise` conda environment using `mamba activate hirise` or `conda activate hirise`.
7. Run `make run` to start the demo process.
8. The demo should automattically launch and the GUI and camera should be displayed on a separate TTY instance. To cycle between TTY instances use ctrl+alt+F# where F# is one of the function keys at the top of your keyboard. Keep in mind that the main TTY is typically on F1 and the secondary TTYs appear on the subsequence function keys so you may have to cycle between them to find the demo again.\
9. You can use a conventional mouse to interact with the GUI and press buttons and modify settings.
10. Run `make kill` to kill the background processes associated with the demo.

## File/Directory Structure

- `scripts/` - A directory containing usefule scripts for converting the UI files to Python and launching the demo.
- `Makefile` - A simple makefile for making the process of running the demo simple

- All relevant demo code and models can be found in the `src` directory
- `src/main.py` - launches the program
- `src/gui.py` - contains the instance of the MainWindow class used to define the GUI controls
- `src/hirise.py` - contains the code relevant to simulating the HiRISE implementation and the baseline implementations for comparison
- `src/ui/` - This directory contains the `pyside6-designer` generated GUI definition in XML
- `src/generated_files/` - This directory contains the converted python files for the GUI

## Important Locations of Changeable Parameters

### Display Resolution

To change the resolution for which the GUI is opened at change the value in `src/main.py` via the following line:

```python
    main_window.resize(1920,1080)
```

### Camera Resolutions

The camera sensor reolutions are stored as a dictionary of integers mapped to corresponding resolutions. You can add or remove values by modifying the following dictionary located in the `__init__` function of `hirise.py`:

```python
    self.camera_resolutions = {
            0: (96, 96),
            1: (100, 100),
            2: (128, 128),
            3: (256, 256),
            4: (320, 320),
            5: (640, 360),
            6: (640, 480),
            7: (800, 600),
            8: (960, 540),
            9: (960, 720),
            10: (1024, 576),
            11: (1280, 720),
            12: (1280, 960),
            13: (1920, 1080),
            14: (2560, 1440),
            15: (3840, 2160)
    }
```

### Pooled Image Sizes

The pooled image sizes must be a multiple of 32. To add or remove pooled image sizes modify the following code in the `__init__` funciton of `hirise.py`:

```python
        self.detection_array_sizes = {}
        for i in range(16):
            self.detection_array_sizes[i] = (i+1)*32
```

Just simply change the number in `range(16)` to increase/decrease the number of pooled image sizes available.

### Compressed Baseline Image Size

The compressed baseline image sizes range from 96x96 to the full resolution of a 4k camera (i.e. 3840x2160). You can add/remove image sizes by modifying the following dictionary in the `__init__` function of `hirise.py`:

```python
    self.baseline_array_sizes = {
            0: (96, 96),
            1: (100, 100),
            2: (128, 128),
            3: (256, 256),
            4: (320, 320),
            5: (640, 360),
            6: (640, 480),
            7: (800, 600),
            8: (960, 540),
            9: (960, 720),
            10: (1024, 576),
            11: (1280, 720),
            12: (1280, 960),
            13: (1920, 1080),
            14: (2560, 1440),
            15: (3840, 2160)
    }
```

### Turn GUI image scaling on/off

By default the demo scales the frames displayed in the GUI visualizers. While this can cause some distortion in image quality it does so homogenously. If you want to test the demo without scaling in the GUI you can simply comment out the following lines in the `update_cameras` funciton at the bottom of the `gui.py`:

```python
        self.ui.detectVideo.setPixmap(detect_pm.scaled(
            detectVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.disabledVideo.setPixmap(baseline_pm.scaled(
            disabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
        self.ui.enabledVideo.setPixmap(hirise_pm.scaled(
            enabledVideoSize, Qt.AspectRatioMode.KeepAspectRatio))
```

## Troubleshooting

### Issues with X libraries

Due to conda/mamba needing to install PySide6 (the GUI platform), it needs to access several X libraries to work properly. However, in our case the version of PySide6 is often incompatible with the XOrg libraries on the system installed via`apt` or could just have a difficult time finding them. To solve this you must add the conda/mamba environment's libraries folder to the system's library path. To do this:

1. Activate the `hirise` environment.
2. Run the following command to add the conda environment's libraries to the system's libraries path:

```shell
#!/bin/bash
export LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}
```

After performing these steps you should be able to run the demo using the following commands:

```shell
xinit &
DISPLAY=:0 python src/main.py &
```

### An xinit instance is already running

Use the following command to kill all instances of `xinit`:

```shell
pkill xinit
```

# Contributors:

This demo was created by Brendan Reidy and Peyton Chandarana.  

If you have any questions regarding the demo, please contact us on LinkedIn.  

Paper Authors:  

Brendan Reidy - University of South Carolina  
Sepehr Tabrizchi - University of Nebraska, Lincoln  
MohammadReza Mohammadi - University of South Carolina  
Shaahin Angizi - New Jersey Institute of Technology  
Arman Roohi - University of Nebraska, Lincoln  
Ramtin Zand - University of South Carolina  

# Paper Citation:

HiRISE: High-Resolution Image Scaling for Edge ML via In-Sensor Compression and Selective ROI  

**_Description:_**  
With the rise of tiny IoT devices powered by machine learning (ML), many researchers have directed their focus toward compressing models to fit on tiny edge devices. Recent works have achieved remarkable success in compressing ML models for object detection and image classification on microcontrollers with small memory, e.g., 512kB SRAM. However, there remain many challenges prohibiting the deployment of ML systems that require high-resolution images. Due to fundamental limits in memory capacity for tiny IoT devices, it may be physically impossible to store large images without external hardware. To this end, we propose a high-resolution image scaling system for edge ML, called HiRISE, which is equipped with selective region-of-interest (ROI) capability leveraging analog in-sensor image scaling. Our methodology not only significantly reduces the peak memory requirements, but also achieves up to 17.7x reduction in data transfer and energy consumption.

```
TBA
```
