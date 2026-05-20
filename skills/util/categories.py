SKILL_CATEGORIES = {

    # messaging
    "rabbitmq": "messaging",
    "kafka": "messaging",
    "sqs": "messaging",
    "sns": "messaging",
    "activemq": "messaging",
    "nats": "messaging",
    "zeromq": "messaging",
    "ibm mq": "messaging",
    "eventbridge": "messaging",
    "pubsub": "messaging",
    "google pubsub": "messaging",
    "apache pulsar": "messaging",

    # databases
    "azure sql": "relational_database",
    "postgresql": "relational_database",
    "mysql": "relational_database",
    "sql server": "relational_database",
    "oracle": "relational_database",
    "mariadb": "relational_database",
    "sqlite": "relational_database",
    "db2": "relational_database",
    "sql": "relational_database",
    "pl/sql": "relational_database",

    # nosql
    "mongodb": "nosql",
    "dynamodb": "nosql",
    "redis": "nosql",
    "firestore": "nosql",
    "cassandra": "nosql",
    "couchbase": "nosql",
    "neo4j": "nosql",
    "elasticsearch": "nosql",
    "nosql": "nosql",

    # cloud
    "oracle cloud": "cloud",
    "aws": "cloud",
    "gcp": "cloud",
    "azure": "cloud",
    "cloud": "cloud",
    "ec2": "cloud",
    "ecs": "cloud",
    "eks": "cloud",
    "lambda": "cloud",
    "s3": "cloud",
    "rds": "cloud",
    "cloud run": "cloud",
    "cloud functions": "cloud",
    "bigquery": "cloud",
    "azure devops": "cloud",
    "firebase": "cloud",

    # backend
    "fastapi": "backend_framework",
    "flaskapi": "backend_framework",
    "flask": "backend_framework",
    "django": "backend_framework",
    "spring": "backend_framework",
    "spring boot": "backend_framework",
    "spring cloud": "backend_framework",
    "spring security": "backend_framework",
    "express": "backend_framework",
    "nestjs": "backend_framework",
    "laravel": "backend_framework",
    "asp.net": "backend_framework",
    ".net": "backend_framework",
    ".net core": "backend_framework",

    # frontend
    "react": "frontend_framework",
    "react.js": "frontend_framework",
    "vue": "frontend_framework",
    "vue.js": "frontend_framework",
    "angular": "frontend_framework",
    "next.js": "frontend_framework",
    "nextjs": "frontend_framework",
    "nuxt": "frontend_framework",
    "svelte": "frontend_framework",
    "jquery": "frontend_framework",

    # mobile
    "flutter": "mobile_framework",
    "react native": "mobile_framework",
    "android": "mobile_framework",
    "ios": "mobile_framework",
    "swift": "mobile_framework",
    "kotlin": "mobile_framework",

    # containers
    "docker": "containerization",
    "podman": "containerization",

    # orchestration
    "kubernetes": "orchestration",
    "openshift": "orchestration",
    "swarm": "orchestration",

    # api
    "rest api": "api",
    "graphql": "api",
    "grpc": "api",
    "soap": "api",
    "openapi": "api",
    "swagger": "api",

    # methodologies
    "scrum": "agile_methodology",
    "jira": "agile_methodology",
    "helix": "agile_methodology",
    "bmc control-m": "agile_methodology",
    "kanban": "agile_methodology",
    "agile": "agile_methodology",
    "devops": "agile_methodology",
    "xp": "agile_methodology",

    # vcs
    "git": "version_control",
    "github": "version_control",
    "gitlab": "version_control",
    "bitbucket": "version_control",

    # ci/cd
    "jenkins": "ci_cd",
    "github actions": "ci_cd",
    "gitlab ci": "ci_cd",
    "circleci": "ci_cd",
    "azure pipelines": "ci_cd",
    "ci/cd": "ci_cd",

    # testing
    "unit testing": "testing",
    "unit test": "testing",
    "e2e testing": "testing",
    "integration test": "testing",
    "e2e": "testing",
    "xunit": "testing",
    "junit": "testing",
    "pytest": "testing",
    "selenium": "testing",
    "cypress": "testing",
    "playwright": "testing",
    "robot framework": "testing",
    "tdd": "testing",
    "bdd": "testing",
    "unix": "testing",

    # architecture
    "microservices": "architecture",
    "solid": "architecture",
    "clean architecture": "architecture",
    "hexagonal architecture": "architecture",
    "ddd": "architecture",
    "soa": "architecture",
    "mvc": "architecture",
    "event driven": "architecture",
    "oop": "architecture",
    "poo": "architecture",
    "clean code": "architecture",
    "design patterns": "architecture",

    # security
    "oauth": "security",
    "oauth2": "security",
    "jwt": "security",
    "keycloak": "security",
    "iam": "security",
    "security": "security",

    # languages
    "python": "language",
    "c": "language",
    "c++": "language",
    "c#": "language",
    "java": "language",
    "go": "language",
    "golang": "language",
    "rust": "language",
    "php": "language",
    "ruby": "language",
    "javascript": "language",
    "typescript": "language",
    "scala": "language",
    "kotlin": "language",
    "swift": "language",

    # markup/style
    "html": "markup",
    "css": "style",
    "sass": "style",
    "scss": "style",
    "tailwind": "style",
    "bootstrap": "style",

    # orm
    "sqlalchemy": "orm",
    "hibernate": "orm",
    "entity framework": "orm",
    "typeorm": "orm",
    "sequelize": "orm",

    # scripting
    "bash": "scripting",
    "shell script": "scripting",
    "powershell": "scripting",

    # data
    "pandas": "data_library",
    "numpy": "data_library",
    "spark": "data_library",
    "airflow": "data_library",
    "hadoop": "data_library",

   # monitoring
    "grafana": "monitoring",
    "prometheus": "monitoring",
    "datadog": "monitoring",
    "new relic": "monitoring",
    "elk": "monitoring",
    "splunk": "monitoring",
    "nagios": "monitoring",
    "zabbix": "monitoring",
    "dynatrace": "monitoring",

    # cache
    "memcached": "cache",
    "redis cache": "cache",

    # search
    "elasticsearch": "search_engine",
    "solr": "search_engine",

    # os
    "linux": "operating_system",
    "ubuntu": "operating_system",
    "windows": "operating_system",
    "unix": "operationg_system",
    "macos": "operationg_system",

    # package managers
    "npm": "package_manager",
    "yarn": "package_manager",
    "pip": "package_manager",
    "poetry": "package_manager",

    # infrastructure as code
    "terraform": "infrastructure_as_code",
    "ansible": "infrastructure_as_code",
    "pulumi": "infrastructure_as_code",

    # observability
    "opentelemetry": "observability",
    "tracing": "observability",
    "logging": "observability",
}