# Use the official RabbitMQ image from the Docker Hub
FROM rabbitmq:3-management-alpine
# Enable the Web STOMP plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable rabbitmq_web_stomp