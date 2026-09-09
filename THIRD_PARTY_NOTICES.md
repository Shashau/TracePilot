# Third-party notices

The project uses the pinned packages in requirements.txt and requirements-dev.txt. Native Windows wheels are redistributed unchanged from their package distributions; their own `.dist-info/licenses`, `LICENSE`, `COPYING`, or license metadata remain in each wheel and apply to those components. See the adjacent SHA256SUMS for file integrity.

Notable dependencies: FastAPI, Starlette, HTTPX, Uvicorn, Pydantic, jsonschema, scikit-learn, NumPy, SciPy, pytest, and their pinned transitive dependencies. This application's licensing does not replace dependency licenses.

Swagger UI distribution version 5.27.1 is bundled for offline REST API documentation. Its Apache 2.0 license, NOTICE, and bundled third-party notices are retained in `app/static/vendor/`.

The application uses operating-system fonts and does not load external fonts, analytics, or an LLM service. The default management Swagger page uses local assets. No external dataset or image assets are included.
