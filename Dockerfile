FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN addgroup --system app && adduser --system --ingroup app app
COPY --chown=app:app . .
RUN mkdir -p /app/instance && chown app:app /app/instance

ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000
EXPOSE 5000

USER app
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '5000') + '/healthz', timeout=2)"]
CMD ["python", "-m", "backend.serve"]
