FROM python:3
MAINTAINER briggs.brenton@gmail.com

WORKDIR /tmp
# Install consul-template
RUN curl https://releases.hashicorp.com/consul-template/0.18.5/consul-template_0.18.5_linux_amd64.tgz -o consul-template.tgz
RUN gunzip consul-template.tgz
RUN tar -xf consul-template.tar
RUN mv consul-template /opt/consul-template
RUN rm -rf /tmp/consul-template*

WORKDIR /usr/src
CMD pip install -r ./requirements.txt && /opt/consul-template --template "config.ini.tmpl:config.ini" -exec "python ./chatbot.py"
