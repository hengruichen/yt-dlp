# yt-dlp Documentation

Welcome to the documentation for yt-dlp! This guide will help you get started with downloading videos from YouTube and other platforms.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Introduction

yt-dlp is a powerful command-line program designed to download videos from YouTube and other video hosting platforms. It supports a wide range of formats and offers extensive customization options.

### Key Features

- Download videos from YouTube and other platforms
- Support for multiple formats (audio, video, subtitles)
- Customizable download options
- Support for playlists and channels
- Advanced filtering and extraction capabilities

---

## Installation

To install yt-dlp, you can use pip:

```bash
pip install yt-dlp
```

Alternatively, you can download the source code and install it manually:

```bash
git clone https://github.com/yt-dlp/yt-dlp.git
cd yt-dlp
pip install -e .
```

---

## Usage

To download a video, use the following command:

```bash
yt-dlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

For more information, see the [documentation](https://github.com/yt-dlp/yt-dlp/wiki).

---

## Configuration

yt-dlp offers a wide range of configuration options to customize your downloads. You can configure yt-dlp using the `--config` option or by creating a configuration file.

### Configuration Options

- `--format`: Specify the format to download (e.g., `best`, `audio`, `video`)
- `--output`: Set the output directory for downloaded files
- `--extractor-args`: Pass arguments to specific extractors
- `--write-sub`: Enable subtitle download
- `--write-auto-sub`: Enable automatic subtitle download
- `--write-info-json`: Save video information in JSON format
- `--write-annotations`: Save video annotations

---

## Advanced Features

yt-dlp offers advanced features for more complex use cases:

### Playlist Downloading

Download all videos from a YouTube playlist:

```bash
yt-dlp --playlist-start 1 --playlist-end 10 https://www.youtube.com/playlist?list=PLXt7w636R7lK6d5jYzXpXpXpXpXpXpXp
```

### Channel Downloading

Download all videos from a YouTube channel:

```bash
yt-dlp --all-formats --playlist-items 1-1000 https://www.youtube.com/channel/UCXt7w636R7lK6d5jYzXpXpXpXpXpXpXp/videos
```

### Custom Download Options

Configure yt-dlp with custom options:

```bash
yt-dlp --format bestaudio --output "%(title)s.%(ext)s" https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Troubleshooting

If you encounter any issues while using yt-dlp, refer to the [troubleshooting guide](https://github.com/yt-dlp/yt-dlp/wiki/Troubleshooting).

---

## Contributing

We welcome contributions from the community! To contribute, please follow the [contributing guidelines](https://github.com/yt-dlp/yt-dlp/blob/master/CONTRIBUTING.md).

---

Thank you for using yt-dlp! We hope you find it useful for your video downloading needs.
