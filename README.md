# Sweetbot maintenance server

This repository contains the code of the REST API server used for F3D maintenance.

## Upload image

Implements a `POST` request to `/upload` endpoint used to copy PNG files to a given folder.
The SHA256 hash of the file is returned and if the file already exists, the file is only touched to update its modification time.

> [!NOTE]
> Only .png files are accepted with a maximum size of 300KB

A symmetric `GET` request to `/upload/<SHA256>` endpoint can be used to retrieve the image.

A `clean.py` is also provided to remove images older than 90 days.

## Mattermost

Implements a `POST` request to `/github` endpoint to convert github events to Mattermost messages.
