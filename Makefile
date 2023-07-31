create_network:
	@docker network create ugc-service-network 2>/dev/null || echo "ugc-service-network is up-to-date"

# prod start
.PHONY: up
up: create_network ## up services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml up -d

.PHONY: logs
logs: ## tail logs services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml down

.PHONY: build
build: ## build services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml build

.PHONY: restart
restart: down up ## restart services

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose -f docker-compose.override.yml -f docker-compose.yml down --remove-orphans --volumes
# prod end

# local start

.PHONY: up-local
up-local: create_network ## up local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.kafka.yml -f docker-compose.override.yml up --build

.PHONY: down-local
down-local: ## down local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.kafka.yml -f docker-compose.override.yml down

.PHONY: build-local
build-local: ## build local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.kafka.yml -f docker-compose.override.yml build --force-rm

.PHONY: build-force-local
build-force-local: ## build force services
	@docker-compose -f docker-compose.local.yml -f docker-compose.kafka.yml -f docker-compose.override.yml build --no-cache

.PHONY: logs-local
logs-local: ## logs local services
	@docker-compose -f docker-compose.local.yml -f docker-compose.kafka.yml -f docker-compose.override.yml logs -f

.PHONY: restart-local
restart-local: down-local up-local ## logs local services

.PHONY: uninstall-local
uninstall-local: ## uninstall local services
	@docker-compose -f docker-compose.override.yml -f docker-compose.local.yml -f docker-compose.kafka.yml down --remove-orphans --volumes

# local end

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

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

# vertica start

.PHONY: up-vertica
up-vertica: create_network
	@docker-compose -f performance_tests/vertica/docker-compose.vertica.yml up --build


.PHONY: uninstall-vertica
uninstall-vertica:
	@docker-compose -f  performance_tests/vertica/docker-compose.vertica.yml down --remove-orphans --volumes

# vertica end