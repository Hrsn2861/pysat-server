FROM python:3.6.9

ENV HOME=/opt/server

WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

RUN apt install libmariadb-dev

COPY . $HOME

EXPOSE 80

ENV PYTHONUNBUFFERED=true
CMD ["/bin/sh", "config/run.sh"]
