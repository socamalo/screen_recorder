import os
from datetime import datetime
from io import BytesIO

import cv2
import keyboard
import numpy as np
import win32clipboard
from mss import mss
from PIL import Image


def setup_directories():
    # Create directories for saving files
    for directory in ["screenshots", "videos"]:
        path = os.path.join(os.getcwd(), directory)  # Use current working directory
        if not os.path.exists(path):
            os.makedirs(path)


def get_monitor_choice():
    # Get monitor information
    with mss() as sct:
        monitors = sct.monitors[
            1:
        ]  # Skip the first one which represents all monitors combined

    print("\nAvailable Monitors:")
    for i, monitor in enumerate(monitors, 1):
        # Get more monitor information
        monitor_info = f"Monitor {i}"

        # Add resolution information
        monitor_info += f" - Resolution: {monitor['width']}x{monitor['height']}"

        # Primary monitor marker
        if monitor["left"] == 0 and monitor["top"] == 0:
            monitor_info += " [Primary Monitor]"

        print(f"{i}. {monitor_info}")

    print("\nNote: Primary monitor is usually the built-in laptop screen")

    while True:
        try:
            choice = int(input("\nSelect monitor (1-{0}): ".format(len(monitors))))
            if 1 <= choice <= len(monitors):
                return choice
            print("Invalid choice, please try again")
        except ValueError:
            print("Please enter a valid number")


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def take_screenshot(monitor_num):
    # Use more readable timestamp format
    timestamp = datetime.now().strftime("%Y-%m-%d %Hh-%Mm-%Ss")
    filename = os.path.join(os.getcwd(), "screenshots", f"screenshot_{timestamp}.png")

    with mss() as sct:
        monitor = sct.monitors[monitor_num]
        screenshot = sct.grab(monitor)
        # Save to file
        image = Image.frombytes(
            "RGB", (screenshot.width, screenshot.height), screenshot.rgb
        )
        image.save(filename)

        # Copy to clipboard
        output = BytesIO()
        image.save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        try:
            send_to_clipboard(win32clipboard.CF_DIB, data)
            print("Screenshot copied to clipboard")
        except Exception as e:
            print(f"Failed to copy to clipboard: {str(e)}")

    print(f"Screenshot saved to: {filename}")


def record_screen(monitor_num):
    # Use more readable timestamp format
    timestamp = datetime.now().strftime("%Y-%m-%d %Hh-%Mm-%Ss")
    filename = os.path.join(os.getcwd(), "videos", f"recording_{timestamp}.mkv")

    # Set higher frame rate
    fps = 30.0  # Increased to 30fps (from original 20fps)

    with mss() as sct:
        monitor = sct.monitors[monitor_num]
        width = monitor["width"]
        height = monitor["height"]

        # Try to set up encoder specifically for MKV format
        # First try FFMPEG backend
        try:
            # Use FFMPEG backend
            fourcc = cv2.VideoWriter_fourcc(
                *"XVID"
            )  # Use XVID encoding in MKV container
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            if not out.isOpened():
                raise Exception("Cannot open VideoWriter")

            print(f"Using XVID encoder with MKV container, framerate: {fps}fps")

        except Exception as e:
            print(f"Failed to use XVID encoder: {e}")
            try:
                # Try MJPG encoder
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

                if not out.isOpened():
                    raise Exception("Cannot open VideoWriter")

                print(f"Using MJPG encoder with MKV container, framerate: {fps}fps")

            except Exception as e:
                print(f"Failed to use MJPG encoder: {e}")
                print("Trying uncompressed format...")

                # Use uncompressed format to ensure recording works
                fourcc = cv2.VideoWriter_fourcc(*"I420")
                out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

                if not out.isOpened():
                    print("All encoders failed, cannot record video")
                    return

                print(f"Using I420 encoder with MKV container, framerate: {fps}fps")

        print("Recording started... Press 'Esc' to stop")
        recording = True

        try:
            while recording:
                # Check global keyboard events
                if keyboard.is_pressed("esc"):
                    recording = False
                    continue

                # Capture screen content
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Write to video file
                out.write(frame)

                # Scale preview window to avoid nested effect
                preview_width = min(800, width)
                preview_height = int(height * (preview_width / width))
                preview_frame = cv2.resize(frame, (preview_width, preview_height))

                # Show preview window
                cv2.imshow("Recording", preview_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        finally:
            out.release()
            cv2.destroyAllWindows()
            print(f"Recording saved to: {filename}")


def main():
    print("Welcome to Screen Recorder!")
    setup_directories()

    while True:
        print("\nPlease select an operation:")
        print("1. Take Screenshot")
        print("2. Record Video")
        print("3. Clean Screenshots Folder")
        print("4. Clean Videos Folder")
        print("5. Exit")

        choice = input("Your choice: ")

        if choice == "5":
            break

        if choice in ["1", "2"]:
            monitor_num = get_monitor_choice()

            if choice == "1":
                take_screenshot(monitor_num)
            else:
                record_screen(monitor_num)
        elif choice == "3":
            clean_directory("screenshots")
        elif choice == "4":
            clean_directory("videos")
        else:
            print("Invalid choice, please try again")


def clean_directory(dir_type):
    """Clean the specified directory"""
    directory = os.path.join(os.getcwd(), dir_type)

    if not os.path.exists(directory):
        print(f"{dir_type} folder does not exist")
        return

    files = os.listdir(directory)

    if not files:
        print(f"{dir_type} folder is already empty")
        return

    print(f"There are {len(files)} files in the folder")
    confirm = input(f"Are you sure you want to delete all {dir_type}? (y/n): ")

    if confirm.lower() == "y":
        for file in files:
            file_path = os.path.join(directory, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        print(f"All {dir_type} files have been deleted")
    else:
        print("Operation cancelled")


if __name__ == "__main__":
    main()
