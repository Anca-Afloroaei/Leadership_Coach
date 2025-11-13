## Install dependencies 

Use the following command
```bash
uv pip install pyproject.toml
```

### Additional Native Dependencies

The development plan PDF export relies on [WeasyPrint](https://weasyprint.org/). On macOS you can install the required libraries via:

```bash
brew install pango cairo gdk-pixbuf libffi
```

Refer to the WeasyPrint documentation for installation guidance on other platforms.

## Running the app while in Development

### Backend

Use the following command to start the development server from inside the backend folder:

```bash
source .venv/bin/activate
uvicorn main:app --reload --app-dir .
```

### Frontend

Use the following command to start the web server from inside the frontend folder:

```bash
npm run dev
```
