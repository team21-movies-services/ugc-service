create_network:
	@docker network create ugc-service-network 2>/dev/null || echo "ugc-service-network is up-to-date"

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# test vertica start

.PHONY: test-up-vertica
test-up-vertica: create_network
	@docker-compose -f ./vertica/docker-compose.vertica.yml up --build

.PHONY: test-uninstall-vertica
test-uninstall-vertica:
	@docker-compose -f  ./vertica/docker-compose.vertica.yml down --remove-orphans --volumes

# vertica end

# test mongo start

.PHONY: test-up-mongo
test-up-mongo: create_network
	@docker-compose -p ugc-service-mongo-test -f ./mongo/docker-compose.mongo.yml up --build -d

.PHONY: test-uninstall-mongo
test-uninstall-mongo:
	@docker-compose -p ugc-service-mongo-test -f ./mongo/docker-compose.mongo.yml down --remove-orphans --volumes

# test mongo end

# perfomance test start

.PHONY: test-up-postgres
test-up-postgres: create_network
	@docker-compose -f ./read_operations/docker.compose.postgres.yml up --build

.PHONY: test-uninstall-postgres
test-uninstall-postgres:
	@docker-compose -f ./read_operations/docker.compose.postgres.yml down --remove-orphans --volumes


.PHONY: run-test-postgres
run-test-postgres: create_network
	@docker-compose -f ./read_operations/docker.compose.postgres.yml run --rm run-postgres-test-perf


.PHONY: test-up-mongo
test-up-mongo: create_network
	@docker-compose -f ./read_operations/docker.compose.mongo.yml up --build

.PHONY: test-uninstall-mongo
test-uninstall-mongo:
	@docker-compose -f ./read_operations/docker.compose.mongo.yml down --remove-orphans --volumes

# perfomance test end
