**Docker-face-detection**
**Real-time face detection in Python using OpenCV and MediaPipe, packaged in Docker for easy deployment.**  

# Face Detector 🧠🎥

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

---

# STATUS

**Version:**  
![Version](https://img.shields.io/badge/Version-1.0-darkblue?style=for-the-badge)

**Supported Platforms:**  
![Debian](https://img.shields.io/badge/Debian_13-Tested-green)
![Linux](https://img.shields.io/badge/Linux-Tested-brightgreen)
![Windows](https://img.shields.io/badge/Windows-Should_Work-yellow)
![MacOS](https://img.shields.io/badge/MacOS-Should_Work-yellow)

**Not Supported:**  
![Android](https://img.shields.io/badge/Android-Not_supported_May_Be_Supported_In_Future-darkred)
![iOS](https://img.shields.io/badge/iOS-Not_supported-darkred)

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

---

# Usage

Note: The repository's Dockerfile is located at docker/main.dockerfile. The examples below reference that path. Also the face detection model is models/detector.tflite and the Dockerfile in this repo copies it into the image.

## METHOD ONE: Build from Source

**Linux:**
```bash
sudo docker build -t giovx/docker-face-detection:1.0 -f docker/main.dockerfile .
```

**Windows:**
Build the Docker image (from repository root):
```powershell
docker build -t giovx/docker-face-detection:1.0 -f docker/main.dockerfile .
```

**btw instead of building from source you can do like this:**
```bash
docker pull giovx/docker-face-detection:1.0
```

If you omit the :1.0 tag, Docker will tag the image as "latest"; the run examples below assume the :1.0 tag used in the build command.

**Run the container:**

**FOR LINUX AND ALSO WINDOWS (using WSL2 + X11 server, e.g., VcXsrv)**

```bash
docker run --rm -it \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  giovx/docker-face-detection:1.0
```

Option 2: Use a Linux VM if WSL2 is not available.


## MacOS:

On MacOS, Docker can run natively, but accessing the webcam and the X server requires some extra steps. Since MacOS does not have X11 by default for GUI forwarding, the recommended way is to either use an X server like XQuartz or run the container inside a Linux virtual machine.

### Option 1: Using XQuartz

1. Install [XQuartz](https://www.xquartz.org/) and start it.
2. Allow connections from network clients:
   - Open **XQuartz > Preferences > Security**.
   - Check **"Allow connections from network clients"**.
3. In your terminal, allow local connections:
```bash
xhost + 127.0.0.1
```

**Build the Docker image**
```bash
docker build -t giovx/docker-face-detection -f main.dockerfile .
```
**then**
```bash
docker run --rm -it \
  -e DISPLAY=host.docker.internal:0 \
  giovx/docker-face-detection:1.0
```
**Option 2: Using a Linux VM**

**Install a lightweight Linux VM (e.g., Ubuntu) via VirtualBox or VMware.**

**Install Docker inside the VM.**

**Build and run the Docker image exactly like you would on Linux:**

```bash
  sudo docker build -t giovx/docker-face-detection -f main.dockerfile .
sudo docker run --rm -it \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  giovx/docker-face-detection:1.0
```

**OR MAYBE JUST USE AN EASY METHOD, DONT DOCKERIZE THE PROJECT AND RUN THE PYTHON FILE, easy**

**SOME PART OF THE README ARE REVISIONED OR WRITTEN BY AIs**

