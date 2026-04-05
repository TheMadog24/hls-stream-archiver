# HLS Stream Archiver

A flexible **HLS recording and archiving tool** designed to capture live HLS streams reliably, store metadata, detect missing segments, and enable later reconstruction of full streams.

This tool is designed as both a **CLI tool and a reusable library** that can be integrated into other projects — including analytics platforms.

### **Not intended for real-time playback.**

---
## In Development / Planning

This is a necessary tool for another project of mine, as well as a learning experience for me.

## Currently Implemented

- CLI interface with arguments
- Basic logging system
- HTTP playlist fetching
- Optional OAuth support
- Error handling(?)
- Playlist Detection


## To Do

### Required
- Download and process HLS segments
- Continuous recording loop
- Handle retries and reconnects
- Save `.ts` segments
- OAuth Validation and reporting
- Full debug/logging support
- Stream quality selection
- Config file support
- Resume interrupted recordings
- Docker Support

### Optional
- (Optional) combined video output
- (Optional) audio-only capture

---

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

## Installation and Usage

To Do...

