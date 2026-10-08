FROM apache/airflow:3.3.2

COPY --from=eclipse-temurin:21-jre /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt