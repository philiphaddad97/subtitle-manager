# SubtitleRenamer

SubtitleRenamer is a Python utility designed to automatically rename subtitle files to match corresponding video files in the same directory. The tool identifies pairs based on the `SxxExx` (season and episode) pattern and renames subtitle files to match the video file names, with a customizable suffix.

## Features

- Identifies video and subtitle pairs by matching episode codes like `S01E01`.
- Case-insensitive pattern matching ensures compatibility with various file naming conventions.
- Customizable subtitle suffix (e.g., "en" for English, "es" for Spanish).
- Supports popular video (`.mkv`, `.mp4`, `.avi`) and subtitle (`.srt`, `.ass`, `.sub`) file formats.
- Custom logging with options to log to console and/or a file.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/SubtitleRenamer.git
    cd SubtitleRenamer
    ```

2. Install dependencies (optional: `typer` is required for the CLI):

    ```bash
    pip install typer
    ```

3. Ensure Python 3.7+ is installed on your system.

## Usage

### Command-Line Interface

SubtitleRenamer provides a CLI for ease of use, allowing you to specify the directory, suffix, and logging options.

```bash
python rename_script.py /path/to/your/folder --suffix en --log-to-file
