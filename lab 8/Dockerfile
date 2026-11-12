FROM python:3.12-slim

WORKDIR /app

COPY supplier.py product.py inventory.py order.py main.py test_lab8.py inventory.json ./

# Default: run the interactive menu (use `docker run -it ...`)
CMD ["python", "main.py"]
