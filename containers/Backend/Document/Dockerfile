FROM python:2-onbuild
#ENV CYCLOPS_ENDPOINT=localhost:port/data
ENV DATABASE_HOST=arkismongopersistent
ENV DATABASE_PORT=30010
EXPOSE 55555
ENTRYPOINT ["python","/usr/src/app/backend.py"]