# Local Jenkins controller with the Docker CLI and Docker Pipeline plugin,
# so the repo's Jenkinsfile can run inside a python:3.12-slim agent container.
FROM jenkins/jenkins:lts-jdk17

USER root
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker

USER jenkins
RUN jenkins-plugin-cli --plugins git workflow-aggregator docker-workflow

# Skip the interactive setup wizard (local, localhost-only instance)
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
