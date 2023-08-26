FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}
COPY app.py config.py credentials lambda_function.py requirements.txt ./
COPY chart ./chart
COPY models ./models
COPY routes ./routes
COPY static ./static
COPY templates ./templates
COPY yahoo ./yahoo  
RUN python -m pip install pip==21.3.1
RUN pip install -r requirements.txt  

CMD [ "lambda_function.lambda_handler" ]
