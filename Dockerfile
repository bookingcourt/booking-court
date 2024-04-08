# Use the official Python image as a base image
FROM selenium/standalone-chrome

# RUN sudo apt update

# RUN sudo apt install python3-pip

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# Install required packages
RUN pip install selenium selenium-wire requests mongoengine

ENV TZ=Asia/Hong_Kong

# Set the working directory
WORKDIR /app

# # Copy your Selenium WebDriver script into the container
# COPY ./test-selenium.py .

# Define the command to execute your script
# CMD ["python", "test-selenium.py"]

# docker build -t selenium-chrome-python3 .
# docker run --rm -it -v %cd%:/app selenium-chrome-python3 bash
# docker run --rm -it -v $(pwd):/app selenium-chrome-python3 bash
# docker run --rm -it -v $(pwd):/app nelify/courtbooking bash


# Set container timezone
# TZ=Hongkong


# docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
