FROM amazonlinux:latest

RUN mkdir /app
WORKDIR /app

COPY /api /app/api
COPY /sharedmodels /app/sharedmodels
COPY /Pipfile /Pipfile.lock /app/

# Pipenv version pinned due to https://github.com/pypa/pipenv/issues/4273
RUN yum upgrade -y && \
    yum install -y shadow-utils python3 which && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    pip install 'pipenv==2018.11.26' && \
    pipenv install --system --deploy --ignore-pipfile && \
    rm Pipfile Pipfile.lock api/Dockerfile && \
    yum clean all && \
    rm -rfv /var/cache/yum && \
    groupadd -r app -g 1042 && \
    useradd -u 1042 -r -g app -m -d /app -s /sbin/nologin -c "App user" app && \
    chown -R app: /app

USER app
CMD ["flask","run", "--host", "0.0.0.0"]
