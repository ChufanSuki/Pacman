# A Dockerfile that sets up a full pacman install with test dependencies
ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION
#RUN apt-get -y update && apt-get install -y unzip libglu1-mesa-dev libgl1-mesa-dev libosmesa6-dev xvfb patchelf ffmpeg cmake swig

# Download mujoco
#RUN mkdir /root/.mujoco && \
#    cd /root/.mujoco  && \
#    curl -O https://www.roboti.us/download/mjpro150_linux.zip && \
#    unzip mjpro150_linux.zip && \
#    echo DUMMY_KEY > /root/.mujoco/mjkey.txt

#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.mujoco/mjpro150/bin

COPY . /usr/local/pacman/
WORKDIR /usr/local/pacman/

RUN pip install -r test_requirements.txt
RUN ["chmod", "+x", "/usr/local/pacman/bin/docker_entrypoint"]

ENTRYPOINT ["/usr/local/pacman/bin/docker_entrypoint"]