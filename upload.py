from flask import Blueprint, request, jsonify, send_from_directory, current_app
import hashlib
import os
from pathlib import Path

bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER"))
UPLOAD_TOKEN = os.getenv("UPLOAD_TOKEN")


@bp.route("/upload", methods=["POST"])
def upload():
    # Token verification is enabled with the --auth argument
    if current_app.config.get("UPLOAD_AUTH"):
        token = request.headers.get("Authorization", "")
        if token != f"Bearer {UPLOAD_TOKEN}":
            return jsonify(error="Unauthorized"), 401

    data = request.get_data()

    # Check PNG signature
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return jsonify(error="Only PNG files are accepted"), 400

    # Check data size
    if len(data) > 300 * 1024:  # 300KB limit
        return jsonify(error="File too large"), 400

    # Name the file after its content hash, so identical uploads share a single file
    sha256 = hashlib.sha256(data).hexdigest()
    destination = UPLOAD_FOLDER / f"{sha256}.png"

    created = not destination.exists()
    if created:
        destination.write_bytes(data)
    else:
        destination.touch()

    return jsonify(success=True, sha256=sha256, size=len(data)), 201 if created else 200


@bp.route("/upload/<file_hash>", methods=["GET"])
def get_upload(file_hash):

    return send_from_directory(UPLOAD_FOLDER, f"{file_hash}.png", mimetype="image/png")
