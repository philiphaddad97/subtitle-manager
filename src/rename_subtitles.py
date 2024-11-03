import os
import re
import logging
from typing import List, Optional


class SubtitleRenamer:
    def __init__(self, directory: str, video_extensions: List[str] = None, subtitle_extensions: List[str] = None, suffix: str = "en", logger=None):
        """
        Initializes the SubtitleRenamer with directory and file extension settings.

        :param directory: Path to the directory containing video and subtitle files.
        :param video_extensions: List of video file extensions to look for (e.g., ['.mkv', '.mp4']).
        :param subtitle_extensions: List of subtitle file extensions to look for (e.g., ['.srt', '.ass']).
        :param suffix: Suffix to append to subtitle files (e.g., 'en' for English).
        :param logger: A logger instance for logging messages.
        """
        self.directory = directory
        self.video_extensions = video_extensions or [".mkv", ".mp4", ".avi"]
        self.subtitle_extensions = subtitle_extensions or [".srt", ".ass", ".sub"]
        self.suffix = suffix
        self.logger = logger or logging.getLogger("SubtitleRenamer")
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logging.DEBUG)

    def _get_files_with_extensions(self, extensions: List[str]) -> List[str]:
        """
        Returns a sorted list of files in the directory matching the specified extensions.

        :param extensions: List of file extensions to filter by.
        :return: Sorted list of filenames with the specified extensions.
        """
        files = sorted(
            [f for f in os.listdir(self.directory) if os.path.splitext(f)[1].lower() in extensions]
        )
        self.logger.debug(f"Found files with extensions {extensions}: {files}")
        return files

    def _extract_and_normalize_episode_pattern(self, filename: str) -> Optional[str]:
        """
        Extracts and normalizes episode patterns from the filename.

        :param filename: The name of the file.
        :return: A normalized pattern like 'S01E01' or None if no match is found.
        """
        # Regex to match episode patterns like S01E01, S01_E01, S1E1, S1_E1, S01E1, S1E01, S01_E1, S01-E01, S1-E1, etc.
        episode_pattern = re.compile(
            r"S(\d{1,2})E(\d{1,2})|S(\d{1,2})_(E)(\d{1,2})|S(\d{1,2})E(\d)|S(\d{1,2})_(E)(\d)|S(\d{1,2})-(E)(\d{1,2})|S(\d{1,2})-(E)(\d)",
            re.IGNORECASE
        )
        match = episode_pattern.search(filename)
        
        if match:
            # Extract season and episode numbers from the match groups
            season = (match.group(1) or match.group(3) or match.group(6) or 
                      match.group(9) or match.group(12)).lstrip('0')  # Remove leading zeros if any
            episode = (match.group(2) or match.group(5) or match.group(8) or 
                       match.group(11) or match.group(13)).lstrip('0')  # Remove leading zeros if any
            
            # Normalize to 'SxxExx' format (e.g., S01E01)
            normalized_code = f"S{int(season):02}E{int(episode):02}"  # Ensure two-digit format
            self.logger.debug(f"Extracted episode code '{normalized_code}' from '{filename}'")
            return normalized_code

    def rename_subtitles(self):
        """
        Renames subtitle files to match corresponding video files, appending a suffix.

        Pairs video and subtitle files based on the episode pattern.
        """
        video_files = self._get_files_with_extensions(self.video_extensions)
        subtitle_files = self._get_files_with_extensions(self.subtitle_extensions)

        # Create mappings with normalized episode codes
        video_mapping = {
            self._extract_and_normalize_episode_pattern(f): f
            for f in video_files
            if self._extract_and_normalize_episode_pattern(f)
        }
        subtitle_mapping = {
            self._extract_and_normalize_episode_pattern(f): f
            for f in subtitle_files
            if self._extract_and_normalize_episode_pattern(f)
        }

        self.logger.debug(f"Video mapping: {video_mapping}")
        self.logger.debug(f"Subtitle mapping: {subtitle_mapping}")

        for episode_code, video_file in video_mapping.items():
            subtitle_file = subtitle_mapping.get(episode_code)
            if subtitle_file:
                self._rename_subtitle(video_file, subtitle_file)
            else:
                self.logger.warning(f"No matching subtitle found for video '{video_file}' with episode code '{episode_code}'")

    def _rename_subtitle(self, video_file: str, subtitle_file: str):
        """
        Renames a single subtitle file to match the corresponding video file, appending the suffix.

        :param video_file: The video file whose name the subtitle will match.
        :param subtitle_file: The subtitle file to rename.
        """
        video_base, _ = os.path.splitext(video_file)
        subtitle_base, subtitle_ext = os.path.splitext(subtitle_file)
        new_subtitle_name = f"{video_base}.{self.suffix}{subtitle_ext}"

        old_subtitle_path = os.path.join(self.directory, subtitle_file)
        new_subtitle_path = os.path.join(self.directory, new_subtitle_name)

        os.rename(old_subtitle_path, new_subtitle_path)
        self.logger.info(f"Renamed '{subtitle_file}' to '{new_subtitle_name}'")
