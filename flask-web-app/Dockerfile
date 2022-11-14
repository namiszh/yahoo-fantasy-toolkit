FROM public.ecr.aws/docker/library/python:3.8.12-slim-buster
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.5.0 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY app.py config.py credentials requirements.txt ./
COPY chart ./chart
COPY models ./models
COPY routes ./routes
COPY static ./static
COPY templates ./templates
COPY yahoo ./yahoo
RUN python -m pip install pip==21.3.1
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b=:80", "-w=1", "app:app"]
