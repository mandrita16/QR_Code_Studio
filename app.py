
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)

import qrcode
import sqlite3
import os
import uuid
import re

from datetime import datetime


# Initialize Flask application
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

OUTPUT_FOLDER = os.path.join(
    BASE_DIR, "static", "generated"
)

DATABASE = os.path.join(BASE_DIR, "qr_history.db")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------- DATABASE ----------------

def get_db_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS qr_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            data TEXT NOT NULL,

            filename TEXT NOT NULL,

            fill_color TEXT NOT NULL,

            back_color TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


# ---------------- VALIDATION ----------------

def valid_color(color):

    return bool(
        re.fullmatch(
            r"#[0-9a-fA-F]{6}",
            color
        )
    )


# ---------------- QR GENERATOR ----------------

def generate_qr(data, fill_color, back_color):

    qr = qrcode.QRCode(

        version=1,

        error_correction=
        qrcode.constants.ERROR_CORRECT_H,

        box_size=10,

        border=4

    )

    qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(

        fill_color=fill_color,

        back_color=back_color

    )

    filename = f"{uuid.uuid4().hex}.png"

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    img.save(filepath)

    return filename


# ---------------- HOME PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def index():

    qr_image = None
    error = None

    data = ""
    fill_color = "#000000"
    back_color = "#F3EFFF"
    if request.method == "POST":

        data = request.form.get(
            "data", ""
        ).strip()

        fill_color = request.form.get(
            "fill_color", "#000000"
        )

        back_color = request.form.get(
            "back_color", "#F3EFFF"
        )

        if not data:

            error = "Please enter some text or URL."

        elif len(data) > 2000:

            error = "Maximum input length is 2000 characters."

        elif not valid_color(fill_color):

            error = "Invalid QR color."

        elif not valid_color(back_color):

            error = "Invalid background color."

        elif fill_color.lower() == back_color.lower():

            error = "QR and background colors must be different."

        else:

            try:

                # Generate QR image
                qr_image = generate_qr(
                    data,
                    fill_color,
                    back_color
                )

                # Save history
                conn = get_db_connection()

                conn.execute(
                    """
                    INSERT INTO qr_history
                    (
                        data,
                        filename,
                        fill_color,
                        back_color,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,

                    (
                        data,
                        qr_image,
                        fill_color,
                        back_color,
                        datetime.now().strftime(
                            "%d-%m-%Y %I:%M %p"
                        )
                    )
                )

                conn.commit()
                conn.close()

            except Exception:

                error = "QR generation failed. Please try again."
                qr_image = None

    # Fetch recent history
    conn = get_db_connection()

    history = conn.execute(
        """
        SELECT *
        FROM qr_history
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()

    conn.close()

    return render_template(

        "index.html",

        qr_image=qr_image,

        history=history,

        error=error,

        data=data,

        fill_color=fill_color,

        back_color=back_color

    )


# ---------------- DOWNLOAD ----------------

@app.route("/download/<filename>")
def download(filename):

    if not re.fullmatch(
        r"[a-f0-9]{32}\.png",
        filename
    ):

        return "Invalid filename", 400

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    if not os.path.isfile(filepath):

        return "QR code not found", 404

    return send_from_directory(

        OUTPUT_FOLDER,

        filename,

        as_attachment=True

    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
