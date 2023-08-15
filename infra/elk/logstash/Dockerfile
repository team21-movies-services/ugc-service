ARG STACK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/logstash/logstash:${STACK_VERSION}

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-codec-json_lines