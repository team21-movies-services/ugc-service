
BASE_DOCKER_COMPOSES = -f docker-compose.yml -f docker-compose.override.yml

# TODO: clickhouse to
LOCAL_DOCKER_COMPOSES = -f docker-compose.local.yml \
	-f docker-compose.mongo.yml \
	-f docker-compose.kafka.yml \
	-f docker-compose.override.yml

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create_network:
	@docker network create ugc-service-network 2>/dev/null || echo "ugc-service-network is up-to-date"
	@docker network create movies-elk-network 2>/dev/null || echo "movies-elk-network is up-to-date"


# prod start
.PHONY: up
up: create_network ## up services
	@docker-compose $(BASE_DOCKER_COMPOSES) up -d

.PHONY: logs
logs: ## tail logs services
	@docker-compose $(BASE_DOCKER_COMPOSES) logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose $(BASE_DOCKER_COMPOSES) down

.PHONY: build
build: ## build services
	@docker-compose $(BASE_DOCKER_COMPOSES) build

.PHONY: restart
restart: down up ## restart services

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose $(BASE_DOCKER_COMPOSES) down --remove-orphans --volumes
# prod end

# local start

.PHONY: up-local
up-local: create_network ## up local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) up --build

.PHONY: up-local-d
up-local-d: create_network ## up all local services in daemon mode
	@docker-compose $(LOCAL_DOCKER_COMPOSES) up --build -d

.PHONY: down-local
down-local: ## down local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) down

.PHONY: build-local
build-local: ## build local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) build --force-rm

.PHONY: build-force-local
build-force-local: ## build force services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) build --no-cache

.PHONY: logs-local
logs-local: ## logs local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) logs -f $(serv)

.PHONY: restart-local
restart-local: down-local up-local ## logs local services

.PHONY: uninstall-local
uninstall-local: ## uninstall local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) down --remove-orphans --volumes

# local end

# kafka start

.PHONY: up-kafka
up-kafka: create_network ## up local services
	@docker-compose -f docker-compose.kafka.yml up --build


.PHONY: uninstall-kafka
uninstall-kafka: ## uninstall all services
	@docker-compose -f docker-compose.kafka.yml down --remove-orphans --volumes

# kafka end

# clickhouse start

.PHONY: up-ch
up-ch: create_network
	@docker-compose -f docker-compose.clickhouse.yml up --build -d


.PHONY: uninstall-ch
uninstall-ch:
	@docker-compose -f docker-compose.clickhouse.yml down --remove-orphans --volumes

# clickhouse end

# test vertica start

.PHONY: test-up-vertica
test-up-vertica: create_network
	@docker-compose -f performance_tests/vertica/docker-compose.vertica.yml up --build


.PHONY: test-uninstall-vertica
test-uninstall-vertica:
	@docker-compose -f  performance_tests/vertica/docker-compose.vertica.yml down --remove-orphans --volumes

# vertica end

# test mongo start

.PHONY: test-up-mongo
test-up-mongo: create_network
	@docker-compose -p ugc-service-mongo-test -f performance_tests/mongo/docker-compose.mongo.yml up --build -d


.PHONY: test-uninstall-mongo
test-uninstall-mongo:
	@docker-compose -p ugc-service-mongo-test -f  performance_tests/mongo/docker-compose.mongo.yml down --remove-orphans --volumes

# test mongo end

# mongo start

.PHONY: up-mongo
up-mongo: create_network
	@docker-compose -f docker-compose.mongo.yml up -d

.PHONY: down-mongo
down-mongo: create_network
	@docker-compose -f docker-compose.mongo.yml down

.PHONY: logs-mongo
logs-mongo: create_network
	@docker-compose -f docker-compose.mongo.yml logs -f

.PHONY: restart-mongo
restart-mongo: down-mongo up-mongo ## restart mongo services

.PHONY: uninstall-mongo
uninstall-mongo: create_network
	@docker-compose -f docker-compose.mongo.yml down --remove-orphans --volumes

# mongo end

# ELK start

.PHONY: up-elk
up-elk:
	@docker-compose -p movies-elk -f ./infra/elk/docker-compose.elk.yml up -d --build

.PHONY: down-elk
down-elk:
	@docker-compose -p movies-elk -f ./infra/elk/docker-compose.elk.yml down

.PHONY: logs-elk
logs-elk:
	@docker-compose -p movies-elk -f ./infra/elk/docker-compose.elk.yml logs -f

.PHONY: restart-elk
restart-elk: down-elk up-elk

.PHONY: uninstall-elk
uninstall-elk:
	@docker-compose -p movies-elk -f ./infra/elk/docker-compose.elk.yml down --remove-orphans --volumes

# ELK end


# FILEBEAT start

.PHONY: up-filebeat
up-filebeat: create_network
	@docker-compose --project-directory . -p ugc-service -f infra/filebeat/docker-compose.filebeat.yml up -d --build

.PHONY: down-filebeat
down-filebeat:
	@docker-compose --project-directory . -p ugc-service -f infra/filebeat/docker-compose.filebeat.yml down

.PHONY: logs-filebeat
logs-filebeat:
	@docker-compose --project-directory . -p ugc-service -f infra/filebeat/docker-compose.filebeat.yml logs -f

.PHONY: restart-filebeat
restart-filebeat: down-filebeat up-filebeat

.PHONY: uninstall-filebeat
uninstall-filebeat:
	@docker-compose --project-directory . -p ugc-service -f infra/filebeat/docker-compose.filebeat.yml down

# FILEBEAT end

# test postgres start

.PHONY: test-up-postgres
test-up-postgres: create_network
	@docker-compose -f ./performance_tests/read_operations/docker.compose.postgres.yml up --build

.PHONY: test-uninstall-postgres
test-uninstall-postgres:
	@docker-compose -f ./performance_tests/read_operations/docker.compose.postgres.yml down --remove-orphans --volumes


.PHONY: run-test-postgres
run-test-postgres: create_network
	@docker-compose -f ./performance_tests/read_operations/docker.compose.postgres.yml run --rm run-postgres-test-perf


# postgres end
