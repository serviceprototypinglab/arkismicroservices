FROM python:2-onbuild
#ENV CYCLOPS_ENDPOINT=localhost:port/data
ENV DATABASE_HOST=arkismongopersistent
ENV DATABASE_PORT=30010
EXPOSE 50004
ENTRYPOINT ["python","/usr/src/app/backend.py"]