FROM python:3.6
# Change to latest python
ENV DJANGO_ENV=${DJANGO_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

COPY ./requirements.txt /
RUN pip install -r requirements.txt
# always copy files after installing packages 
# docker will cache the packages hence better build time
WORKDIR /code

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
ADD ./entrypoint_beat /entrypoint_beat
ADD ./entrypoint_django /entrypoint_django
ADD ./entrypoint_worker /entrypoint_worker


RUN chmod +x /entrypoint_django
RUN chmod +x /entrypoint_beat
RUN chmod +x /entrypoint_worker

# always copy files after installing packages
# docker will cache the packages hence better build time
COPY . /code
EXPOSE 8000
RUN chmod +x /wait