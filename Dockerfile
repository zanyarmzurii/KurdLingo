FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set Python Path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the bot
CMD ["python", "-m", "bot.main"]
