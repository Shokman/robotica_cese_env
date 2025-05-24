# syntax=docker/dockerfile:1
ARG ROS_DISTRO=jazzy
 
FROM osrf/ros:${ROS_DISTRO}-desktop as base
ENV ROS_DISTRO=${ROS_DISTRO}
SHELL ["/bin/bash", "-c"]

RUN set -euo pipefail
ENV DEBIAN_FRONTEND=noninteractive

# Get Ubuntu packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    tmux \
    git \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create workspace
RUN mkdir -p /root/ros2_ws/src
WORKDIR /root/ros2_ws/src
COPY src /root/ros2_ws/src
RUN vcs import < mycobot.repos

# Install dependencies
RUN apt-get update -y && apt-get install -y \
  ros-${ROS_DISTRO}-moveit \
  ros-${ROS_DISTRO}-gz-tools-vendor \
  ros-${ROS_DISTRO}-gz-sim-vendor
# See https://gazebosim.org/docs/latest/ros2_gz_vendor_pkgs/

# Compile the workspace
WORKDIR /root/ros2_ws
RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
  && rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
  && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --symlink-install

# Create env for converting rosbags
RUN apt-get update -y && apt-get install -y \
  python3-pip python3.12-venv \
  && python3 -m venv .venv && source .venv/bin/activate \
  && pip3 install rosbags && deactivate

# Configure entrypoint
COPY ./entrypoint.sh /
RUN chmod +x  /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["bash"]
