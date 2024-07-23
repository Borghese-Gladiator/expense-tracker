FROM python:3.10-slim

ARG LUNCH_MONEY_API_KEY
ENV LUNCH_MONEY_API_KEY=$LUNCH_MONEY_API_KEY

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Borghese-Gladiator/expense-tracker.git .

WORKDIR /app/client

RUN pip3 install virtualenv
RUN virtualenv venv
RUN /bin/bash -c "source venv/bin/activate && pip3 install -r requirements.txt"

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/bin/bash", "-c", "source venv/bin/activate && streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
# RUN make run_streamlit
