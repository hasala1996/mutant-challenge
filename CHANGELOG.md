# CHANGELOG

## [0.0.1] - 2024-11-12
- Initial release of the Mutant Detection API following Hexagonal Architecture principles.
  - **Endpoints**:
    - `/mutant/`: Endpoint to check if a DNA sequence belongs to a mutant. Returns a success message if the DNA is mutant, and a 403 error if not.
    - `/stats/`: Endpoint to retrieve statistics about mutant and human DNA sequences stored in the database.
  - **Core Services**:
    - `MutantService`: Handles DNA verification and interaction with repositories to determine if a DNA sequence is mutant or human.
  - **Repositories**:
    - Abstract and concrete repositories for DNA storage and retrieval in a PostgreSQL database.
  - **Database**:
    - Migration setup with Alembic to create necessary tables and manage database schema.
  - **Testing**:
    - Comprehensive unit and integration tests covering endpoints, services, and database interactions.
    - Test coverage is at 90%.
