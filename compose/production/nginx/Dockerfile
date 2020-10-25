FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
EXPOSE 80
COPY ./compose/production/nginx/sites-enabled/gdrive.conf /etc/nginx/sites-enabled/default
