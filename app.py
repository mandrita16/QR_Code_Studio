
from flask import Flask, render_template, request
import qrcode
import re
import base64
import logging

from io import BytesIO
from datetime import datetime


# ---------------- APPLICATION ----------------

app = Flask(__name__)

app.logger.setLevel(logging.INFO)


# Temporary in-memory history
qr_history = []


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

        error_correction=qrcode.constants.ERROR_CORRECT_H,

        box_size=10,

        border=4

    )

    qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(

        fill_color=fill_color,

        back_color=back_color

    )

    # Generate image in memory
    buffer = BytesIO()

    img.save(buffer, format="PNG")

    buffer.seek(0)

    # Convert image to Base64
    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return encoded_image


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

                # Generate QR code
                qr_image = generate_qr(
                    data,
                    fill_color,
                    back_color
                )

                # Save temporary history
                record = {

                    "data": data,

                    "filename": "qr-studio-code.png",

                    "fill_color": fill_color,

                    "back_color": back_color,

                    "created_at": datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    )

                }

                qr_history.insert(0, record)

                # Keep only the latest 10 records
                del qr_history[10:]

            except Exception as e:

                app.logger.exception(
                    "QR generation failed"
                )

                error = "QR generation failed. Please try again."

                qr_image = None

    return render_template(

        "index.html",

        qr_image=qr_image,

        history=qr_history,

        error=error,

        data=data,

        fill_color=fill_color,

        back_color=back_color

    )


# ---------------- HEALTH CHECK ----------------

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "QR Studio"
    }


# ---------------- LOCAL DEVELOPMENT ----------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
