# AutoCartOS: Multi-Agent Autonomous Purchasing System

A hackathon-grade, production-inspired multi-agent system that converts high-level user goals into complete, compatible product bundles using a controlled agent pipeline.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python api.py

# Or run example directly
python example.py
```

## API Usage

```bash
curl -X POST http://localhost:8000/generate-cart \
  -H "Content-Type: application/json" \
  -d '{"user_goal": "I want to set up a home office for remote work"}'
```

## System Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## Key Features

- **6 Specialized Agents**: Intent → Planner → Dependency → Compatibility → Product Selection → Cart Composer
- **Rule-Based Logic**: Deterministic dependency and compatibility validation
- **LLM Integration**: Used only for natural language understanding and planning
- **Complete Bundles**: Ensures all dependencies are satisfied
- **Compatibility Validation**: Prevents incompatible component combinations
- **Explainable**: Each agent's output is traceable through shared state

## Project Structure

```
.
├── state.py           # Shared state definition
├── agents.py          # All 6 agent implementations
├── rules.py           # Dependency & compatibility rules
├── graph.py           # LangGraph orchestration
├── api.py             # FastAPI backend
├── catalog.json       # Product catalog
├── example.py         # Example usage
└── ARCHITECTURE.md    # Detailed architecture docs
```

## Why This Is Not a Chatbot

- **Deterministic Pipeline**: Fixed agent sequence with clear responsibilities
- **Structured Output**: JSON state updates, not conversational responses
- **Rule-Based Validation**: Compatibility and dependencies use explicit rules
- **Complete Bundles**: System ensures completeness, not just recommendations
- **Explainable**: Each agent's contribution is visible in the state

