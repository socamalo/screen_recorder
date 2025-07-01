# Screen Recorder

A powerful and user-friendly screen recording tool built with Python that allows you to capture screenshots and record videos from multiple monitors.

## Features

- **Multi-Monitor Support**: Detect and use any connected monitor
- **Screenshot Capture**:
  - Save screenshots in PNG format
  - Automatic clipboard copy
  - Timestamp-based file naming
- **Video Recording**:
  - High-quality MKV video format
  - 30 FPS recording
  - Live preview window
  - Multiple video codec support (XVID, MJPG, I420)
- **File Management**:
  - Organized file storage in dedicated folders
  - Built-in cleanup utilities
  - Timestamp-based file naming

## Requirements

- Python 3.7+
- Windows OS (due to win32clipboard dependency)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/socamalo/screen_recorder.git
cd screen-recorder
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python main.py
```

### Main Menu Options:

1. **Take Screenshot**: Capture a still image of the selected monitor
2. **Record Video**: Start video recording of the selected monitor
3. **Clean Screenshots Folder**: Remove all screenshots
4. **Clean Videos Folder**: Remove all recorded videos
5. **Exit**: Close the application

### Controls

- Press `Esc` to stop video recording
- Press `q` to quit the preview window

### Output Files

- Screenshots are saved in the `screenshots` folder
- Videos are saved in the `videos` folder
- Files are automatically named with timestamps (format: YYYY-MM-DD HHh-MMm-SSs)

## Dependencies

- opencv-python: Video processing and recording
- numpy: Array operations
- mss: Screen capture
- Pillow: Image processing
- keyboard: Keyboard event handling
- pywin32: Windows clipboard operations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the MSS library for efficient screen capture
- OpenCV community for video processing capabilities
- All contributors and users of this project
