FROM ubuntu:latest
FROM python:3.7
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]

# For Flask Application
# CMD ["app/steam_analytics.py"] 

# For Plotly Dash Application
CMD ["app/steam_analytics_dash.py"]  