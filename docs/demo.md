# Record a demonstration

1. Build the package and run `roslaunch edge_detection_node canny.launch rqt:=true`.
2. Play the original bag or another compatible ROS image source.
3. Arrange the original image, edge image, and parameter controls so all are visible.
4. Record approximately 15–30 seconds. Start with defaults, change `th1` and `th2`, then change `blur_ksize` using odd values such as 1, 5, and 9.
5. Check that the recording shows actual updates and readable controls.
6. Save one screenshot as `assets/canny-preview.png`. Create `assets/` only when the actual image is available.
7. Add `![Camera image and Canny edge map in RViz](assets/canny-preview.png)` after the README introduction once the file exists.
8. Add a short clip to the README through GitHub's attachment interface, or store a compact GIF as `assets/canny-demo.gif` and embed it.

Do not claim real-time performance or a frame rate without measurement on identified hardware. Record the input source, ROS version, and parameters used if adding a performance result. The original source bag and conversion procedure are not included in this repository.
