import typer

from custom_logger import CustomLogger
from rename_subtitles import SubtitleRenamer

app = typer.Typer()

@app.command()
def rename_subtitles(
    directory: str = typer.Argument(..., help="Path to the directory containing video and subtitle files."),
    suffix: str = typer.Option("ar", help="Suffix to append to subtitle files (default: 'en')."),
    log_to_file: bool = typer.Option(False, help="If set, logs will also be saved to a file.")
):
    """
    Rename subtitle files in the given directory to match the video files with an optional suffix.
    """
    # Instantiate the custom logger
    custom_logger = CustomLogger(name="SubtitleRenamerLogger", log_to_file=log_to_file).get_logger()
    
    # Instantiate and use the SubtitleRenamer with command-line arguments
    renamer = SubtitleRenamer(directory=directory, suffix=suffix, logger=custom_logger)
    renamer.rename_subtitles()

if __name__ == "__main__":
    app()
