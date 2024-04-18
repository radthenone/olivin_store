FROM redis:7.2

COPY ./docker/redis/init.sh /redis/init.sh
RUN sed -i 's/\r$//g' /redis/init.sh && chmod +x /redis/init.sh

WORKDIR /redis

EXPOSE 6379

CMD ["./init.sh"]
