# Raw Data Directory

This directory is intended to store raw, unprocessed data files that might be used as input for the PVS (Prime Vector Space) project.

## Contents

- **Source of data:** Describe where the raw data comes from (e.g., downloaded prime lists, experimental results, etc.).
- **Format:** Specify the format of the files (e.g., CSV, TXT, binary).
- **Preprocessing steps:** If any manual or minimal preprocessing is done before these files are considered "raw" for the automated pipeline, describe it here.

## Usage

Files in this directory should typically be treated as read-only by the main processing scripts. Scripts should read from `data/raw/` and write processed output to `data/processed/` or other appropriate locations.

**Note:** Large raw data files should ideally not be committed directly to the Git repository. Instead, consider using Git LFS (Large File Storage) or storing them in a separate data management system and providing instructions here on how to obtain them. If they are small or essential for basic examples, they might be included.

Currently, this directory is a placeholder.
