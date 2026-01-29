# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) principles.

---

## [1.2.0] - 2026-01-29

### Added

- Rebranding from "Quiron" to "ArgusVision" to better reflect the project's vision and capabilities.
- Updated documentation and README to reflect the new project name and branding.
- Comprehensive unit test suite using `pytest` and `pytest-cov` in the `tests/` directory.
- Hand gesture recognition logic in `src/argusvision/logic/gestures/hands.py`:
    - Added support for "Peace Sign", "Good Job" (Thumb Up), and "Disapproval" (Thumb Down).
- Movement persistence and filtering logic in `HandEngine` to stabilize hand tracking.
- Interactive Dashboard UI implemented with PySide6 in `src/argusvision/ui/dashboard.py`.
- High-performance vectorized hand skeleton `Renderer` in `src/argusvision/engine/renderer.py`.

### Changed

- Project structure migrated to a modern `src/` layout.
- Switched dependency management and packaging to `Poetry`.

## [1.1.0] - 2023-04-06

### Changed

- Separated functions and constants into modular files: `gestures.py` and `constants.py`.

<!-- markdownlint-configure-file { "MD022": false, "MD024": false, "MD030": false, "MD032": false} -->
