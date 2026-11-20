FROM python:3.12-slim

WORKDIR /app

COPY *.py products.csv inventory.json ./
COPY tests/ ./tests/

# Default: run the interactive menu (use `docker run -it ...`)
# Run the tests with: docker run --rm lab9 python -m unittest discover -s tests -v
CMD ["python", "main.py"]
