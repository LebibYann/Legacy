# GeneWeb

**Migration/modernization of an OCaml genealogy application to a Python 3 (backend) + Svelte 5 (frontend) stack.**





## Context and Goals

### Why the migration?

GeneWeb is a powerful genealogy software originally written in OCaml. While the OCaml implementation has proven robust and performant over the years, we are migrating to modern technologies to address several key challenges:

- **Maintainability**: Python offers a larger developer community and more accessible codebase for future contributors
- **Modern tooling**: Leverage contemporary development tools, testing frameworks, and deployment practices
- **Infrastructure simplification**: Reduce deployment complexity with containerized Python/Svelte stack
- **Enhanced compatibility**: Better integration with modern web technologies and third-party services
- **Developer adoption**: Lower barrier to entry for new team members and contributors

### Final objective

Deliver a new version of GeneWeb with equivalent (or improved) functionality while preserving the core genealogy algorithms and data integrity that users depend on. The migration will maintain backward compatibility with existing databases and provide a clear migration path for current users.





## Overall Architecture

The project is organized into distinct components that facilitate both the legacy system consulting and testing as well as the new implementation development:

```
.
├── geneweb/            # Legacy OCaml code
├── geneweb_docker/     # Dockerfiles and configs to run the legacy project
├── new_geneweb/        # New backend (Python) + frontend (Svelte)
├── tests/              # End-to-end and integration tests
├── docs/               # Technical and functional documentation
├── TESTING.md          # Guide to run and write tests
├── CONTRIBUTING.md     # Contribution guidelines
└── README.md           # This file
```

You can have more detail on new project [here](new_geneweb/README.md).



## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Docker**: Version 20.10+ with Docker Compose
- **Python**: 3.13+
- **Node.js**: 20+

### Package Managers
- **Python**: poetry
- **Node.js**: npm
- **OCaml**: opam (only for legacy code)





## Running the Legacy Project

The original OCaml-based GeneWeb can be run using Docker:

```bash
cd geneweb_docker
docker compose up --build
```

Access the legacy application at `http://localhost:2316` (setup) and `http://localhost:2317` (user)





## Installing & Running the New Project

### Docker
```bash
docker compose up --build
```

### Manual
Follow the respective readme files in each component directory.
- [Backend](new_geneweb/backend/README.md)
- [Frontend](new_geneweb/frontend/README.md)
- [Backoffice](new_geneweb/backoffice/README.md)
- [Database](new_geneweb/database/README.md)





## Testing

Comprehensive testing documentation is available in [`TESTING.md`](TESTING.md).

### Quick Test Commands
- **Backend tests**: `cd new_geneweb/backend && poetry run pytest`
- **Frontend tests**: `cd new_geneweb/frontend && pnpm test`
- **End-to-end tests**: `cd tests/end-to-end && pnpm run test`
- **Functional tests**: `cd tests/functional && python -m pytest`





## Running the docker

To run the Docker containers for the New Geneweb project, you can use the provided `docker-compose.yml` file at the root of this project. Make sure you have Docker and Docker Compose installed on your machine.

### Standard Profiles

```bash
# Production with HTTPS (default)
docker compose --profile prod up --build

# Ephemeral with HTTPS (temporary database)
docker compose --profile ephemeral up --build

# HTTP without SSL (no certificate warnings)
docker compose --profile http up --build
```

### Development Mode

```bash
# Development with HTTPS
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Reset database (Fresh Database Every Time)

To quickly get idem-potent behavior with a fresh database on every startup, use the provided scripts:

**Windows (Batch / CMD):**
```cmd
./scripts/clear-docker-db.bat
```

**Linux/Mac (Bash):**
```bash
sh ./scripts/clear-docker-db.sh
```

📖 **See [nginx/README.md](nginx/README.md) for HTTPS/HTTP configuration details**

## Documentation

Technical and functional documentation is organized in the [`docs/`](docs/README.md) folder:

All documentation is written in plain Markdown for easy reading and contribution.





## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Checklist
- **Branch naming**: `feature/description` or `fix/description`
- **Code style**:
  - Python: Follow PEP 8, use `black` and `isort`
  - TypeScript/Svelte: Use Prettier and ESLint
  - OCaml: Follow existing project conventions
- **Testing**: Add tests for new features and bug fixes
- **Documentation**: Update relevant docs for user-facing changes
- **PR process**: Create detailed pull requests with clear descriptions





## Roadmap / Project Status

### Completed ✅
- Legacy OCaml codebase analysis and documentation
- Docker containerization for legacy system
- New project structure setup
- Backend API foundation (Python/FastAPI)
- Frontend scaffolding (Svelte)
- Basic testing infrastructure

### In Progress ⏳
- Reimplementation of core feature
- Core genealogy algorithms migration
- Database schema design and migration tools
- API endpoint implementation
- Mobile-responsive design





## License

This project is licensed under the GPL-2.0 License - see the original GeneWeb license for details.
