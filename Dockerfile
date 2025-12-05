# 1. Base Image (Lightweight Python)
FROM python:3.9-slim

# 2. Set Working Directory inside the container
WORKDIR /app

# 3. Copy Requirements & Install Dependencies
# (Age requirements copy korchi jate Docker cache use korte pare)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Entire Project
# (Host machine theke container er vitore sob copy hobe)
COPY . .

# 5. Run Setup Script
# (Jodi kono folder missing thake, eta create kore dibe)
RUN python setup_final.py

# 6. Expose API Port
EXPOSE 8000

# 7. Start Command (Production Mode)
# (Correct syntax for Uvicorn)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
