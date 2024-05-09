# app/Dockerfile

FROM python:3.12

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     nmap \
#     && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin/:$PATH"

# create a venv
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY requirements.txt requirements.txt
RUN uv pip install -r requirements.txt


COPY ./src /app/src

EXPOSE 8080

ENTRYPOINT ["python", "src/main.py"]
