# Docker Face Detection

Real-time face detection using OpenCV and MediaPipe packaged into a reproducible Docker image for consistent deployment and testing.

Badges  
![Python](https://img.shields.io/badge/Python-3.11-blue) ![License](https://img.shields.io/badge/License-Apache%202.0-green) ![Version](https://img.shields.io/badge/Version-1.0-darkblue?style=for-the-badge)

---

## Table of contents


- [Features](#features)
- [Architecture & Components](#architecture--components)
- [Requirements](#requirements)
- [Build (from source)](#build-from-source)
- [Run (container)](#run-container)
  - [Linux / macOS (X11 display)](#linux--macos-x11-display)
  - [Windows (WSL2 + X11 server)](#windows-wsl2--x11-server)
  - [Headless / Server (no GUI)](#headless--server-no-gui)
  - [Optional: GPU acceleration (NVIDIA)](#optional-gpu-acceleration-nvidia)
- [Configuration & environment variables](#configuration--environment-variables)
- [Operational notes & troubleshooting](#operational-notes--troubleshooting)
- [Development & extending](#development--extending)
- [License](#license)

---
# Technologies Used

This project leverages modern tools and libraries for real-time face detection:

| Library | Version | Badge |
|---------|---------|-------|
| Python | 3.11 | ![Python](https://img.shields.io/badge/python-3.11-blue) |
| OpenCV | 4.12.0 | ![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-brightgreen) |
| MediaPipe | 0.10.31 | ![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.31-orange) |
| NumPy | 2.2.6 | ![NumPy](https://img.shields.io/badge/NumPy-2.2.6-blueviolet) |
| sounddevice | 0.5.3 | ![sounddevice](https://img.shields.io/badge/sounddevice-0.5.3-lightgrey) |
| Other libraries | absl-py 2.3.1, cffi 2.0.0, flatbuffers 25.12.19, pycparser 2.23, setuptools 79.0.1, wheel 0.45.1 | - |





## Features

- Real-time face detection from webcam (V4L2 / /dev/video* on Linux)
- Bounding boxes and optional landmark overlays (via MediaPipe)
- Audio or other hooks can be added (project includes sounddevice in dependencies list)
- Single Dockerfile to build a reproducible runtime image

---


## Architecture & Components

- Application: Python script(s) that initialize a MediaPipe graph for face detection, handle video capture via OpenCV, draw overlays and optionally play/trigger audio.
- Container: Debian-based runtime with Python 3.11 and pinned Python dependencies to ensure deterministic behavior.
- I/O: Video input via host device /dev/video* (Linux) or via virtualized device when using VM/WSL. Video output displayed through X11 forwarding or captured for headless processing.

---

**Supported Platforms:**  
![Debian](https://img.shields.io/badge/Debian_13-Tested-green)
![Linux](https://img.shields.io/badge/Linux-Tested-brightgreen)
![Windows](https://img.shields.io/badge/Windows-Should_Work-yellow)
![MacOS](https://img.shields.io/badge/MacOS-Should_Work-yellow)

**Not Supported:**  
![Android](https://img.shields.io/badge/Android-Not_supported_May_Be_Supported_In_Future-darkred)
![iOS](https://img.shields.io/badge/iOS-Not_supported-darkred)

---

## Requirements

Host:
- Docker Engine (20.x+ recommended)
- For GUI display:
  - Linux: Native X11 socket
  - Windows: WSL2 + an X11 server (VcXsrv, Xming)
- Optional for GPU:
  - NVIDIA GPU + nvidia-container-toolkit (for containerized CUDA support)
  - 

Container:
- Python 3.11
- OpenCV 4.12.0
- MediaPipe 0.10.31
- NumPy 2.2.6
- sounddevice 0.5.3 (optional)

Dependency versions are pinned in the Dockerfile used to build the image for reproducibility.

---

## Build (from source)

Build the Docker image using the repository Dockerfile `main.dockerfile`:

Linux / macOS:
```bash
sudo docker build -t giovx/docker-face-detection:1.0 -f main.dockerfile .
```

Windows (PowerShell):
```powershell
docker build -t giovx/docker-face-detection:1.0 -f main.dockerfile .
```

Notes:
- Use the `-t` tag to version your image.
- If you modify dependency pins, rebuild to get deterministic behavior.

---

## Run (container)

### Linux / macOS (X11 display)

Run with access to a local webcam (/dev/video0) and the X11 socket to display windows on the host:

```bash
# Allow the container to use the host display
xhost +local:docker

docker run --rm -it \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  giovx/docker-face-detection:1.0
```

Explanation of flags:
- `--device=/dev/video0:/dev/video0` exports the webcam device into the container.
- `-e DISPLAY=$DISPLAY` passes the display address.
- `-v /tmp/.X11-unix:/tmp/.X11-unix:rw` mounts the X11 socket for GUI forwarding.
- `--rm -it` interactive mode and automatic cleanup.

After running, GUI windows created by OpenCV will appear on the host X11 server.

### Windows (WSL2 + X11 server)

1. Install and run an X11 server (e.g., VcXsrv).
2. In WSL2 shell configure DISPLAY to point to host (or use `export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0`).
3. Run the same docker command from a WSL2-enabled Docker context (or from PowerShell with appropriate permissions). Example (from WSL2):

```bash
xhost +local:docker

docker run --rm -it \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  giovx/docker-face-detection:1.0
```

Windows specifics:
- Accessing physical webcams from Windows into WSL2 can be non-trivial. Using a Linux VM may be simpler for camera passthrough.
- You may need to forward the appropriate device or use a virtual camera driver that WSL2 can access.

### Headless / Server (no GUI)

If you only need to run detection and output results via logs or a socket (no display), run the container without X11 volumes and change the application to not spawn GUI windows or to save frames to disk:

```bash
docker run --rm -it \
  --device=/dev/video0:/dev/video0 \
  giovx/docker-face-detection:1.0 \
  python main.py --headless
```

(Assumes `main.py` supports a `--headless` flag or an environment variable to disable GUI.)

### Optional: GPU acceleration (NVIDIA)

If you have an NVIDIA GPU and want to enable hardware acceleration for OpenCV or other CUDA-enabled libraries, use the NVIDIA container runtime and ensure the image is built with CUDA-enabled base image and dependencies. Example run command with nvidia runtime:

```bash
docker run --rm -it --gpus all \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  giovx/docker-face-detection:1.0
```

Notes:
- You must build an image that includes CUDA toolkits and compatible binary wheels for dependencies; the current `main.dockerfile` targets CPU runtime unless explicitly modified.
- Use `nvidia-container-toolkit` on the host to enable `--gpus` support.

---

## Configuration & environment variables

Recommended environment variables:
- `DISPLAY` — X11 display address (passed from host for GUI)
- `VIDEO_DEVICE` — e.g., `/dev/video0` (if your entrypoint supports variable device selection)
- `HEADLESS` — set to `1` to disable GUI windows (if supported by application)

Application-level configuration:
- Detection confidence thresholds (MediaPipe) and frame resizing parameters should be set in the application code or via CLI flags to trade off accuracy vs throughput.

---

## Operational notes & troubleshooting

- Black/Blank window or no image:
  - Ensure the X11 socket is mounted (`/tmp/.X11-unix`) and `DISPLAY` is set.
  - On Linux, run `xhost +local:docker` to permit connections from the container.
- Camera not found:
  - Verify host access: `ls /dev/video*`.
  - If using a VM or WSL, ensure USB passthrough or virtual camera is correctly configured.
- High CPU usage / low FPS:
  - Reduce frame resolution before processing (scale frames down).
  - Adjust MediaPipe detection/landmark model parameters to lower compute.
- MediaPipe errors:
  - Confirm dependency binary compatibility (the Dockerfile pins tested versions).
- If you want persistent logs, mount a host volume and write logs to a file inside the container.

---

## Development & extending

- To change detection parameters or add functionality (face recognition, tracking, or callbacks), modify the Python source and rebuild the image.
- Add unit tests for critical processing functions (e.g., bounding box calculations).
- To use in production, consider:
  - Exposing an HTTP/REST (or gRPC) endpoint that accepts frames and returns detection metadata.
  - Running as a headless microservice with a message queue for high throughput.
  - Using hardware acceleration and batch processing to reduce per-frame latency.

---

## Files of interest

- `main.dockerfile` — primary Dockerfile used to build the image
- `app/` or root Python scripts — main application entrypoint(s)
- `requirements.txt` or pinned dependencies inside `main.dockerfile`

---

## License

Apache 2.0

---

## Contact / Next steps

If you want, I can:
- Commit this README to a new branch and open a pull request.
- Update the Dockerfile to include optional CUDA support or a minimal `--headless` entrypoint.
- Add runtime examples for CI or a GitHub Actions workflow to build and publish images.

Tell me which action you prefer and the branch name if you want me to commit.
