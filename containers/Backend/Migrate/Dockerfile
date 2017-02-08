FROM python:2-onbuild
# COPY kubectl /usr/local/bin/kubectl
# RUN chmod +x /usr/local/bin/kubectl
ENV DATABASE_HOST=arkismongopersistent
ENV DATABASE_PORT=30010
EXPOSE 55555
ENTRYPOINT ["python","/usr/src/app/arkismigrate.py"]

