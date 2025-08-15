# Use Maven with Java 11
FROM maven:3.9.6-eclipse-temurin-11

WORKDIR /app
COPY . /app

RUN mvn -B clean test

CMD ["mvn", "test"]
