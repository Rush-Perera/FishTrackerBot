
## Description

FishTrackerBot is a project that integrates image processing, machine learning, and motion control to track fish and navigate a robot accordingly. The project uses a Raspberry Pi, OpenCV for image processing, and GPIO for motor control.
![Fish Image](output\17.png)

## Files

- `motor_control.py`: Contains the code for controlling the robot's motors and processing images to determine the fish's orientation.
- `centerplot.py`: Processes images to find the center positions of the fish and plots them.
- `segmentation.py`: Segments the fish from the images and identifies the head and tail positions.

## Setup

1. **Install Dependencies**:
    - OpenCV
    - NumPy
    - Matplotlib
    - RPi.GPIO (for Raspberry Pi)

    You can install these dependencies using pip:

    ```sh
    pip install opencv-python numpy matplotlib RPi.GPIO
    ```

2. **Setup Raspberry Pi GPIO Pins**:
    - Connect the motors to the GPIO pins as specified in [motor_control.py](http://_vscodecontentref_/6).

3. **Prepare Image Data**:
    - Place the images you want to process in the [snaps](http://_vscodecontentref_/7) folder.

## Usage

1. **Motor Control**:
    - Run [motor_control.py](http://_vscodecontentref_/8) to start the robot and track the fish based on the captured images.

    ```sh
    python motor_control.py
    ```

2. **Center Plot**:
    - Run [centerplot.py](http://_vscodecontentref_/9) to process images and plot the center positions of the fish.

    ```sh
    python centerplot.py
    ```

3. **Segmentation**:
    - Run [segmentation.py](http://_vscodecontentref_/10) to segment the fish from the images and identify the head and tail positions.

    ```sh
    python segmentation.py
    ```

## Output

- Processed images with bounding boxes, head, and tail positions are saved in the [output](http://_vscodecontentref_/11) folder.
- Center positions of the fish are plotted using Matplotlib.

## License

This project is licensed under the MIT License.
