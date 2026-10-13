# ROS Canny Edge Detection

A ROS 1 image-processing project by **Yazdan Bayat**. A Python node subscribes to camera images, applies Gaussian smoothing and OpenCV Canny edge detection, and publishes the resulting edge map. Filter parameters can be adjusted while the node runs using `dynamic_reconfigure`.

The original project targets KITTI camera topics and includes an RViz configuration for viewing the camera stream and edge map together. Other compatible ROS image streams can be used through topic remapping.

## What this project demonstrates

- ROS image subscription and publication using `rospy` and `sensor_msgs/Image`.
- Conversion between ROS images and OpenCV arrays using `cv_bridge`.
- Grayscale conversion, optional Gaussian smoothing, and Canny edge detection.
- Live adjustment of the blur kernel and both Canny thresholds.
- Preservation of the input image header, including timestamp and frame ID.
- Image visualization in RViz and playback of an external ROS bag.

This is a classical computer-vision integration project. It does not train a model, classify objects, or implement autonomous navigation. No accuracy or processing-rate benchmark is provided.

## Processing steps

1. Receive an image and convert it to BGR8.
2. Convert the BGR image to grayscale.
3. Apply Gaussian blur when the kernel size is greater than 1.
4. Run `cv2.Canny` with the configured thresholds.
5. Publish a `mono8` edge map with the original message header.

## Environment

The original project instructions specify **Ubuntu 20.04.6 LTS, ROS Noetic, and Python 3**. Use an existing Noetic environment with the ROS apt repository configured. The commands below are not a complete operating-system or ROS repository installation guide.

ROS Noetic [reached end of life on May 31, 2025](https://discourse.ros.org/t/ros-noetic-end-of-life-may-31-2025/43160). This repository preserves the ROS 1 implementation; it is not a ROS 2 package.

## Repository layout

| Path | Purpose |
|---|---|
| `scripts/edge_detection.py` | ROS image-processing node |
| `cfg/Canny.cfg` | Dynamic-reconfigure parameter definitions |
| `launch/canny.launch` | Launch node, optional RViz, and optional tuning interface |
| `rviz/canny.rviz` | Original RViz camera/edge display configuration |
| `CMakeLists.txt` | Catkin configuration, parameter generation, and installation |
| `package.xml` | Package metadata and dependency declarations |
| `docs/demo.md` | Procedure for recording an actual demonstration |
| `docs/publishing.md` | Initial GitHub publication checklist |
| `docs/preparation-notes.md` | Packaging changes and validation scope |
| `.gitignore` | Excludes build products, local data, and bags |

The GitHub repository is named `ros-canny-edge-detection`; the ROS package name remains **`edge_detection_node`**. Keep that package name: the Python node imports the generated `edge_detection_node.cfg.CannyConfig` module.

## Dependencies and build

Install these dependencies in the configured Ubuntu 20.04 / ROS Noetic environment:

```bash
sudo apt update
sudo apt install -y \
  ros-noetic-catkin \
  ros-noetic-rospy \
  ros-noetic-sensor-msgs \
  ros-noetic-cv-bridge \
  ros-noetic-dynamic-reconfigure \
  ros-noetic-roslaunch \
  ros-noetic-rosbag \
  ros-noetic-rviz \
  ros-noetic-rqt-reconfigure \
  python3-opencv
```

After this repository has been published:

```bash
source /opt/ros/noetic/setup.bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/YzdnByat/ros-canny-edge-detection.git
cd ros-canny-edge-detection
chmod +x scripts/edge_detection.py cfg/Canny.cfg
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

If using a downloaded ZIP instead, extract the repository folder into `~/catkin_ws/src/` and run the same permission and build commands. The root `package.xml` must be inside the extracted repository folder; do not leave the source inside a ZIP.

## Run with a ROS bag

**The input bag is not included.** The original instructions reference `kitti_2011_09_26_drive_0002_synced.bag`, but do not provide a download URL or the conversion settings used to produce it. Obtain the original bag separately or supply another ROS 1 bag containing a compatible raw image topic. See the [KITTI raw-data website](https://www.cvlibs.net/datasets/kitti/raw_data.php) for the original dataset; downloading its raw files alone does not produce this ROS bag.

### Terminal 1: node and visualization

```bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
roslaunch edge_detection_node canny.launch rqt:=true
```

`roslaunch` starts a ROS master if necessary. RViz opens with the supplied configuration. In the parameter interface, select `/edge_detection_node`.

### Terminal 2: playback

Replace the example path with the actual bag location:

```bash
source /opt/ros/noetic/setup.bash
rosbag info /absolute/path/to/input.bag
rosbag play --loop /absolute/path/to/input.bag
```

Expected default input: `/kitti/camera_color_left/image_raw`. When messages arrive, RViz should display the original image and a monochrome edge map. Changing a parameter affects subsequent images; there is no processing until an input image is received.

### Other image topics

```bash
roslaunch edge_detection_node canny.launch \
  input_topic:=/camera/image_raw \
  output_topic:=/camera/canny \
  rviz:=false
```

The input must be a `sensor_msgs/Image` convertible to BGR8. Compressed-image topics require a separate decompression/republishing step. The saved RViz configuration still refers to the default KITTI topics: edit both Image Topic fields if using custom topics.

## Parameters

| Parameter | Default | Range | Effect |
|---|---:|---:|---|
| `blur_ksize` | 5 | 1–31 | Gaussian kernel width and height; 1 skips blur |
| `th1` | 100 | 0–500 | First Canny hysteresis threshold |
| `th2` | 200 | 0–500 | Second Canny hysteresis threshold |

Use odd blur values. The original node rounds an even value upward internally but returns the unmodified configuration to the tuning interface, so the displayed value can differ from the effective kernel size. For predictable tuning, keep `th1 <= th2`.

## ROS interface

| Direction | Default topic | Message | Encoding |
|---|---|---|---|
| Input | `/kitti/camera_color_left/image_raw` | `sensor_msgs/Image` | Converted to `bgr8` |
| Output | `/kitti/camera_color_left/canny_det` | `sensor_msgs/Image` | `mono8` |

The publisher and subscriber use `queue_size=1`. This is not a guarantee of a particular throughput or latency.

## Troubleshooting

- **Package not found:** build the catkin workspace and source its `devel/setup.bash` in the terminal used to launch the node.
- **Cannot import `CannyConfig`:** `Canny.cfg` generates Python code during the catkin build. Rebuild and source the workspace; do not try to install that module through pip.
- **No images:** inspect the bag with `rosbag info`, check topics using `rostopic list`, and verify input activity using `rostopic hz /kitti/camera_color_left/image_raw`.
- **RViz fixed-frame warning:** the original configuration uses `map`, which a camera-only bag may not publish. The two Image displays do not require the 3D grid; disable the grid and use an available frame if needed.
- **Script is not executable:** run the `chmod` command in the build instructions, particularly after extracting on Windows.

## Demonstration and validation status

The uploaded source did not contain a screenshot, video, bag, or measured performance results. [Demo instructions](docs/demo.md) describe how to record the actual application. No illustrative output is presented as an experimental result.

The repository preparation was checked for Python syntax, XML structure, file paths, and preservation of the supplied node, parameter definition, and RViz configuration. A Noetic catkin build and end-to-end bag playback have not been executed as part of this preparation.

## Author and licensing

**Yazdan Bayat** — [GitHub](https://github.com/YzdnByat) · [LinkedIn](https://www.linkedin.com/in/yazdan-bayat-171b23267/)

The uploaded package contained an unset license and a placeholder maintainer email. Complete both metadata fields using [the publication checklist](docs/publishing.md). This preparation does not introduce an open-source license grant.
