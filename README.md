# HLS Stream Archiver

A flexible **HLS recording and archiving tool** designed to capture live HLS streams reliably, store metadata, detect missing segments, and enable later reconstruction of full streams.

This tool is designed as both a **CLI tool and a reusable library** that can be integrated into other projects — including analytics platforms.

### **Not intended for real-time playback.**

---
## In Development / Planning

## Features

- **HLS recording**
  - Downloads HLS segments (`.ts`) from live streams
  - Stores metadata for each segment (timestamps, duration, sequence)
  - Detects missing segments and gaps

- **Gap detection + reconstruction**
  - Marks missing video segments
  - Supports patching gaps using existing VODs or alternative sources
  - Includes overlap buffering for smooth transitions

- **Structured metadata store**
  - JSON metadata for streams and segments
  - UTC-based timestamps

- **CLI + Library**
  - Usable as a command-line tool
  - Importable as a library for other applications
 

---

## Installation


### Clone the repository
```
git clone https://github.com/TheMadog24/hls-stream-archiver.git

cd hls-stream-archiver
```

#### (Optional) Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
#### Install dependencies
```
pip install -r requirements.txt
```
