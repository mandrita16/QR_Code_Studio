# 💜 QR Studio – QR Code Generator

QR Studio is a customizable QR Code Generator built using Python and Flask. It allows users to generate QR codes from text and website URLs, customize QR and background colors, preview generated codes, and download them as PNG images. The application also maintains recent generation history using SQLite, featuring a responsive black-and-purple user interface.

## ✨ Features

- **QR Code Generation:** Convert text and website URLs into QR codes.
- **Color Customization:** Choose custom foreground and background colors.
- **Live Preview:** View generated QR codes directly on the dashboard.
- **PNG Download:** Download generated QR codes as image files.
- **QR History:** Store and retrieve recently generated QR codes using SQLite.
- **Responsive UI:** Dark-themed black and purple interface with a responsive layout.
- **Input Validation:** Validate user input and hexadecimal color values.
- **Unique Filenames:** Generate unique filenames for QR images.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| qrcode | QR code generation |
| Pillow | Image processing |
| SQLite | Database and QR history |
| HTML5 | Frontend structure |
| CSS3 | Styling and responsive design |

## 📂 Project Structure

```text
QR_Studio/
│
├── app.py
├── requirements.txt
├── README.md
├── qr_history.db
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    │
    └── generated/
        └── generated_qr_images.png
```

*Note: `qr_history.db` and generated QR images are created automatically when the application runs.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mandrita16/QR_Studio.git
```

### 2. Navigate to the project directory

```bash
cd QR_Studio
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Git Bash:**

```bash
source venv/Scripts/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

Visit:

```text
http://127.0.0.1:5000
```

## 🚀 How It Works

1. Enter text or a website URL in the input field.
2. Choose your preferred QR code and background colors.
3. Click **Generate QR Code**.
4. Preview the generated QR code.
5. Download the QR code as a PNG image.
6. Access recently generated QR codes through the history section.

## 🧠 Application Architecture

```text
              USER
                |
                v
         Flask Web Interface
                |
                v
          Input Validation
                |
                v
        Python QR Generator
                |
                v
          qrcode Library
                |
                v
         PNG Image Creation
                |
          +-----+------+
          |            |
          v            v
      Image Storage   SQLite
          |            |
          +-----+------+
                |
                v
         QR Preview & Download
```

## 🔮 Future Enhancements

- Wi-Fi QR code generation.
- Email and contact QR codes.
- Logo insertion inside QR codes.
- QR history deletion and management.
- User authentication and personalized QR history.
- Deployment to a cloud platform.

## 🔒 Security Notes

- Input length and color formats are validated.
- Parameterized SQL queries are used for database operations.
- Generated files use unique filenames.
- Flask debug mode is intended for local development only.

## 👩‍💻 Author

**Mandrita Dasgupta**

- GitHub: [@mandrita16](https://github.com/mandrita16)

---

⭐ If you find this project useful, consider giving it a star!

**Built with Python 💜**
