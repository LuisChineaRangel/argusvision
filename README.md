# ArgusVision

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=LuisChineaRangel_argusvision&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=LuisChineaRangel_argusvision)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=LuisChineaRangel_argusvision&metric=coverage)](https://sonarcloud.io/summary/new_code?id=LuisChineaRangel_argusvision)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=LuisChineaRangel_argusvision&metric=bugs)](https://sonarcloud.io/summary/new_code?id=LuisChineaRangel_argusvision)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=LuisChineaRangel_argusvision&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=LuisChineaRangel_argusvision)

---

**ArgusVision** is a high-performance computer vision system for real-time video processing and analysis.
It provides a modular framework for hand tracking, gesture recognition, and interactive visualization using MediaPipe and PySide6.

---

## Table of Contents

- [Current Status](#current-status)
- [Project Structure](#project-structure)
- [Core Features](#core-features)
    - [Hand Tracking Engine](#hand-tracking-engine)
    - [Gesture Recognition](#gesture-recognition)
    - [Real-time Renderer](#real-time-renderer)
- [Installation](#installation)
- [Developer Guide](#developer-guide)

---

## Current Status

- **Stable Version**: v1.2.0
- **Logic**: Fully implemented gesture validation and geometry utilities.
- **Engine**: Integrated MediaPipe Hand Landmarker with movement persistence.
- **UI**: Dashboard with real-time feedback and FPS monitoring.
- **Testing**: Python-based test suite with unit coverage across core modules.
- **Gesture Library**:
    - Peace Sign
    - Thumbs Up (Good Job)
    - Thumbs Down (Disapproval)
    - Finger Counting (0-5)

---

## Project Structure

The project is organized into the following main directories:

- `src/argusvision/engine/`: Core CV processing, including `HandEngine` and vectorized `Renderer`.
- `src/argusvision/logic/`: Math utilities, gesture definitions, and validation logic.
- `src/argusvision/ui/`: Interactive dashboard built with PySide6.
- `assets/mp_models/`: Pre-trained MediaPipe task models.
- `tests/`: Automated test suite for cross-platform validation.
- `scripts/`: Development and utility scripts.

---

## Core Features

### Hand Tracking Engine

The **Hand Tracking Engine** utilizes MediaPipe's Task API to perform real-time landmark detection. It includes native support for:

- **Movement Persistence**: Sophisticated filtering to avoid flickering during detection.
- **Vectorized Transformation**: Efficiently maps 3D landmarks to 2D screen coordinates.

### Gesture Recognition

A rule-based recognition system that analyzes hand geometry. The **GestureValidator** compares sub-segments of the hand (PIP, DIP, and TIP landmarks) to identify complex human poses like:

- **Peace Sign**: Verification of index and middle finger extension with multi-finger exclusion.

Each gesture is mapped to clear, actionable labels (e.g., "Good Job" instead of just "Thumb Up").

### Real-time Renderer

A high-performance rendering layer built on OpenCV that provides:

- **Hand Skeletonization**: Dynamic drawing of skeletal structures with depth-simulated shadows.
- **Sub-pixel Anti-aliasing**: Clean visualizations even at low resolutions.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LuisChineaRangel/argusvision

# Install dependencies using Poetry
poetry install
```

## Developer Guide

To run the application in development mode:

```bash
poetry run argusvision
```

To execute the test suite:

```bash
poetry run pytest
```
