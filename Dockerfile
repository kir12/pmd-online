FROM python:3.11.5

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
# NOTE: for some reason makefile won't allow declaring environmental variables, so UID and GID are hardcoded here
# run id -u and id -g respectively if problems arise
# RUN apt update && \
#     apt install -y libc6 sudo && \
#     addgroup --gid 1000 nonroot && \
#     adduser --uid 1000 --gid 1000 --disabled-password --gecos "" nonroot && \
#     echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Set the non-root user as the default user
# USER nonroot

# WORKDIR /home/nonroot/app
# COPY --chown=nonroot:nonroot . /home/nonroot/app
# RUN mkdir /home/nonroot/mydos
# RUN tar -zxf compile/dosemu-1.4.0.tgz -C /home/nonroot/mydos/
# RUN tar -zxf compile/dosemu-1.4.0-bin.tgz -C /home/nonroot/mydos/
# RUN cd /home/nonroot/mydos/dosemu && chmod 777 * && ./dosemu -dumb

WORKDIR /root/app
COPY . .

RUN apt update && apt install -y libasound2 libgpm2 libsdl1.2debian libslang2 libsndfile1 libxxf86vm1 xfonts-utils xorg xdotool
# dosemu was taken off debian and its binaries are inoperative, so I manually downloaded the .deb file
RUN dpkg -i compile/dosemu_1.4.0.7+20130105+b028d3f-2_amd64.deb
RUN apt-get install -f
# usage: xdotool key Enter | dosemu -dumb "CMD"

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
EXPOSE 8000
