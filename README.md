# MCP Matrix Knowledge System 🥋

> "I need to know Kung Fu" → *downloads module* → "I know Kung Fu!"

Trinity-style downloadable AI knowledge modules. Package any crawled knowledge, blockchain-verified, instantly downloadable by any AI agent.

## Vision

Inspired by The Matrix, this system enables AI agents to instantly acquire new skills and knowledge by downloading pre-packaged modules. No more lengthy context loading or FMR - just download what you need, when you need it.

## Core Features

- **Knowledge Packaging**: Convert crawled web content into portable `.mkm` (Matrix Knowledge Module) files
- **Blockchain Registry**: Decentralized catalog of available knowledge modules
- **Instant Downloads**: AI agents can acquire new expertise in seconds
- **Cryptographic Verification**: Every module is hash-verified for integrity
- **Version Control**: Track knowledge updates and maintain multiple versions

## Use Cases

### Crisis Corps Field Deployment
```python
# Robot arrives at earthquake site
await robot.download_skill("earthquake-search-rescue-protocols")
await robot.download_skill("haitian-creole-language-pack")  
await robot.download_skill("port-au-prince-infrastructure-2025")
# Robot now has all needed knowledge for the mission
```

### New Claude Instance
```python
# Fresh Claude with no memory
await claude.download_skill("jordan-ehrig-projects-june-2025")
await claude.download_skill("mcp-orchestrator-expertise")
# Claude instantly has full project context!
```

### Developer Onboarding
```python
# New team member
await dev.download_skill("company-coding-standards")
await dev.download_skill("revit-api-mastery")
# Instantly productive!
```

## Architecture

```
mcp-matrix-knowledge/
├── packager/           # Creates .mkm files from crawled content
├── registry/           # Blockchain interface for module catalog
├── loader/            # Downloads and installs knowledge modules
├── storage/           # IPFS/S3 distributed storage handlers
├── contracts/         # Smart contracts for module registry
└── examples/          # Sample knowledge modules
```

## Module Format (.mkm)

Each Matrix Knowledge Module contains:
- `metadata.json` - Name, description, skills provided, prerequisites
- `embeddings.pkl` - Vector embeddings for RAG
- `knowledge_graph.dump` - Neo4j export (if applicable)
- `sources.json` - Original URLs and crawl metadata
- `manifest.json` - Installation instructions

## Integration

- **mcp-crawl4ai-rag**: Content acquisition and crawling
- **mcp-memory-blockchain**: Registry and verification
- **mcp-orchestrator**: Natural language module discovery
- **mcp-time-precision**: Version timestamping

## Quick Start

```bash
# Package current memory as a module
python packager/create_module.py --name "my-project-context" --source memory

# Upload to registry
python registry/upload.py --module my-project-context.mkm

# Download in new instance
python loader/download.py "my-project-context"
```

## Roadmap

- [x] Repository setup
- [ ] Basic packager implementation
- [ ] Module format specification
- [ ] Memory export functionality
- [ ] Blockchain registry contracts
- [ ] IPFS storage integration
- [ ] Download manager
- [ ] MCP server interface
- [ ] Orchestrator integration

## The Future

Imagine a world where:
- AI agents share specialized knowledge freely
- No AI starts from scratch - they download what they need
- Knowledge becomes truly portable and verifiable
- Teams collaborate by sharing knowledge modules
- Every piece of AI knowledge has cryptographic provenance

Welcome to the Matrix. 🔴💊