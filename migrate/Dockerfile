FROM amazonlinux:latest

RUN mkdir /app
WORKDIR /app

COPY /migrate /app/migrate
COPY /sharedmodels /app/sharedmodels
COPY /Pipfile /Pipfile.lock /app/

# Pipenv version pinned due to https://github.com/pypa/pipenv/issues/4273
RUN yum upgrade -y && \
    yum install -y shadow-utils python3 which snappy-devel.x86_64 python3-devel.x86_64 && \
    yum groupinstall -y "Development Tools" && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    pip install 'pipenv==2018.11.26' && \
    pipenv install --system && \
    pip3 install black && \
    rm Pipfile Pipfile.lock migrate/Dockerfile && \
    yum remove -y snappy-devel.x86_64 python3-devel.x86_64 && \
    yum groupremove -y "Development Tools" && \
    yum clean all && \
    rm -rfv /var/cache/yum && \
    groupadd -r app -g 1042 && \
    useradd -u 1042 -r -g app -m -d /app -s /sbin/nologin -c "App user" app && \
    chown -R app: /app

USER app
ENTRYPOINT ["python3", "-m", "alembic.config", "--config", "migrate/alembic.ini"]
CMD ["upgrade", "head"]
