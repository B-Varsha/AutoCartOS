# AutoCartOS: Multi-Agent Autonomous Purchasing System

AI-powered industrial procurement assistant.

This Flutter app connects to our FastAPI multi-agent backend and generates smart industrial carts based on user problems. The Flutter Frontend provides the interactive interface that allows users to communicate their needs and visualize the engineered product bundles. It is designed to transform complex JSON data into a clean, actionable industrial procurement dashboard.

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

See [DESIGN_DOCUMENT.md](DESIGN_DOCUMENT.md) for detailed system design.

## Key Features

- **6 Specialized Agents**: Intent → Planner → Dependency → Compatibility → Product Selection → Cart Composer
- **Rule-Based Logic**: Deterministic dependency and compatibility validation
- **LLM Integration**: Used for perception and planning
- **Complete Bundles**: Ensures all dependencies are satisfied
- **Compatibility Validation**: Prevents incompatible component combinations
- **Explainable**: Each agent's output is traceable through shared state

## Frontend Project Structure
```
lib/
├── services/
│   └── api_service.dart      # Handles the HTTP connection to the FastAPI backend
├── widgets/
│   ├── logo.dart             # Branding and visual identity components
│   ├── product_card.dart     # Individual item display with specs and price
│   └── summary_card.dart     # Displays total price and the "Completeness Score"
└── main.dart                 # Application entry point and global state management

```
## Backend Project Structure
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

- **Orchestrated Agentic Pipeline**: Fixed sequence of specialized agents with isolated responsibilities
- **Structured Output**: JSON state updates, not conversational responses
- **Rule-Based Validation**: Compatibility and dependencies use explicit rules
- **Complete Bundles**: System ensures completeness, not just recommendations
- **Explainable**: Each agent's contribution is visible in the state


