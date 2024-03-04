FROM spark:3.5.1-scala2.12-java17-python3-ubuntu

WORKDIR /opt/application
COPY requirements.txt .
RUN pip3 install -r requirements

COPY src/ src/

COPY main.py .