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

The project is organized into distinct components that facilitate both the legacy system maintenance and the new implementation development:

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

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Docker**: Version 20.10+ with Docker Compose
- **Python**: 3.12+
- **Node.js**: 20+

### Package Managers
- **Python**: Poetry (preferred) or pip
- **Node.js**: pnpm (preferred) or npm
- **OCaml**: opam (for legacy code maintenance)

## Installation & Usage

### Running the Legacy Project

The original OCaml-based GeneWeb can be run using Docker:

```bash
cd geneweb_docker
docker-compose up -d
```

Access the legacy application at `http://localhost:2317`

### Running the New Project

#### Backend (Python)
```bash
cd new_geneweb/backend
poetry install
poetry run python -m app.main
```

#### Frontend (Svelte)
```bash
cd new_geneweb/frontend
pnpm install
pnpm run dev
```

#### Backoffice (Svelte)
```bash
cd new_geneweb/backoffice
pnpm install
pnpm run dev
```

### Common Commands
- `docker-compose up -d` - Start legacy services
- `make test` - Run all tests
- `pnpm run build` - Build frontend for production
- `poetry run pytest` - Run backend tests

## Testing

Comprehensive testing documentation is available in [`TESTING.md`](TESTING.md).

### Quick Test Commands
- **Backend tests**: `cd new_geneweb/backend && poetry run pytest`
- **Frontend tests**: `cd new_geneweb/frontend && pnpm test`
- **End-to-end tests**: `cd tests/end-to-end && pnpm run test`
- **Functional tests**: `cd tests/functional && python -m pytest`

## Documentation

Technical and functional documentation is organized in the [`docs/`](docs/README.md) folder:


- **Architecture**: System design and component interactions
- **Algorithms**: Core genealogy algorithms and calculations
- **Binaries**: Command-line tools documentation
- **Formats**: Data formats and schemas
- **Operations**: Deployment and maintenance guides

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
