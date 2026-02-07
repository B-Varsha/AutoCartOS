"""
CartPilot Agent Implementations
Each agent has a single responsibility and updates shared state.
"""
import json
from typing import Dict, Any, List
from state import CartPilotState
from rules import get_dependencies, check_compatibility, validate_component_set, get_all_dependencies


class LLMInterface:
    """Abstracted LLM interface for LangChain compatibility."""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def invoke(self, prompt: str, response_format: str = "json") -> Dict[str, Any]:
        """
        Invoke LLM with prompt. Returns structured JSON.
        In production, this would use LangChain's LLM interface.
        """
        if self.llm is None:
            # Fallback for demo: simple rule-based parsing
            return self._fallback_parse(prompt)
        
        # Real implementation would be:
        # response = self.llm.invoke(prompt)
        # return json.loads(response.content)
        return self._fallback_parse(prompt)
    
    def _fallback_parse(self, prompt: str) -> Dict[str, Any]:
        """Fallback parser for demo purposes."""
        # This is a simplified parser - in production, use actual LLM
        if "home office" in prompt.lower() or "remote work" in prompt.lower():
            return {
                "category": "home_office",
                "use_case": "remote_work",
                "constraints": []
            }
        elif "gaming" in prompt.lower():
            return {
                "category": "gaming",
                "use_case": "gaming_setup",
                "constraints": []
            }
        return {
            "category": "general",
            "use_case": "work",
            "constraints": []
        }


# Global LLM instance (would be injected in production)
llm = LLMInterface()


def intent_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 1: Intent Agent
    Purpose: Parse user goal into structured intent
    Uses LLM: Yes (for natural language understanding)
    """
    user_goal = state["user_goal"]
    
    prompt = f"""
    Parse the following user goal into structured intent:
    "{user_goal}"
    
    Return JSON with:
    - category: primary category (home_office, gaming, creative, etc.)
    - use_case: specific use case
    - constraints: list of any constraints mentioned
    
    Example: {{"category": "home_office", "use_case": "remote_work", "constraints": []}}
    """
    
    parsed_intent = llm.invoke(prompt)
    
    state["parsed_intent"] = parsed_intent
    return state


def planner_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 2: Planner Agent
    Purpose: Generate list of required components based on intent
    Uses LLM: Yes (for component planning)
    """
    parsed_intent = state["parsed_intent"]
    
    prompt = f"""
    Based on this intent: {json.dumps(parsed_intent)}
    
    Generate a list of required components for a complete setup.
    Return JSON array of component names.
    
    Example: ["monitor", "keyboard", "mouse", "desk", "chair"]
    """
    
    # LLM would return list, but for demo we use rule-based mapping
    intent_category = parsed_intent.get("category", "general")
    
    component_mapping = {
        "home_office": ["monitor", "keyboard", "mouse", "desk", "chair", "laptop"],
        "gaming": ["gaming_monitor", "gaming_keyboard", "gaming_mouse", "gaming_headset", "desk", "chair"],
        "creative": ["monitor", "keyboard", "mouse", "desk", "chair", "laptop", "webcam"],
    }
    
    # In production: llm_response = llm.invoke(prompt)
    # For demo: use rule-based mapping
    required_components = component_mapping.get(intent_category, ["monitor", "keyboard", "mouse", "desk"])
    
    state["required_components"] = required_components
    return state


def dependency_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 3: Dependency Agent
    Purpose: Identify all dependencies for required components
    Uses LLM: No (rule-based)
    """
    required_components = state["required_components"]
    
    # Get all dependencies using rule engine
    component_dependencies = get_all_dependencies(required_components)
    
    # Find missing dependencies
    all_required_deps = set()
    for deps in component_dependencies.values():
        all_required_deps.update(deps)
    
    existing_components = set(required_components)
    missing_dependencies = [dep for dep in all_required_deps if dep not in existing_components]
    
    state["component_dependencies"] = component_dependencies
    state["missing_dependencies"] = missing_dependencies
    
    return state


def compatibility_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 4: Compatibility Agent
    Purpose: Check compatibility between all components
    Uses LLM: No (rule-based)
    """
    required_components = state["required_components"]
    missing_deps = state["missing_dependencies"]
    
    # Combine all components
    all_components = required_components + missing_deps
    
    # Build compatibility matrix
    compatibility_matrix = {}
    compatibility_issues = []
    
    for comp1 in all_components:
        compatibility_matrix[comp1] = {}
        for comp2 in all_components:
            if comp1 != comp2:
                is_compatible = check_compatibility(comp1, comp2)
                compatibility_matrix[comp1][comp2] = is_compatible
                if not is_compatible:
                    compatibility_issues.append({
                        "component1": comp1,
                        "component2": comp2,
                        "issue": "Incompatible components"
                    })
    
    state["compatibility_matrix"] = compatibility_matrix
    state["compatibility_issues"] = compatibility_issues
    
    return state


def product_selection_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 5: Product Selection Agent
    Purpose: Select specific products from catalog for each component
    Uses LLM: Yes (for intelligent product matching)
    """
    import json
    from pathlib import Path
    
    # Load catalog
    catalog_path = Path(__file__).parent / "catalog.json"
    with open(catalog_path) as f:
        catalog = json.load(f)
    
    required_components = state["required_components"]
    missing_deps = state["missing_dependencies"]
    all_components = required_components + missing_deps
    compatibility_issues = state["compatibility_issues"]
    
    selected_products = {}
    product_alternatives = {}
    
    # For each component, select a product
    for component in all_components:
        # Map component names to catalog categories
        category_mapping = {
            "monitor": "monitor",
            "gaming_monitor": "monitor",
            "keyboard": "keyboard",
            "gaming_keyboard": "keyboard",
            "mouse": "mouse",
            "gaming_mouse": "mouse",
            "desk": "desk",
            "chair": "chair",
            "laptop": "laptop",
            "monitor_stand": "monitor_stand",
            "hdmi_cable": "hdmi_cable",
            "usb_cable": "usb_cable",
            "laptop_stand": "laptop_stand",
            "external_keyboard": "external_keyboard",
            "external_mouse": "external_mouse",
            "usb_c_adapter": "usb_c_adapter",
            "docking_station": "docking_station",
            "webcam": "webcam",
            "speakers": "speakers",
            "audio_cable": "audio_cable",
            "gaming_headset": "gaming_headset",
        }
        
        catalog_category = category_mapping.get(component, component)
        
        if catalog_category in catalog["products"]:
            products = catalog["products"][catalog_category]
            
            # Filter by compatibility tags if needed
            compatible_products = []
            for product in products:
                tags = product.get("compatibility_tags", [])
                # Check if product tags match component requirements
                if component in tags or any(tag in component for tag in tags):
                    compatible_products.append(product)
                elif not tags:  # No tags means universal compatibility
                    compatible_products.append(product)
            
            if compatible_products:
                # Select first compatible product (in production, LLM would rank)
                selected_products[component] = compatible_products[0]
                product_alternatives[component] = compatible_products[1:] if len(compatible_products) > 1 else []
            elif products:
                # Fallback to any product in category
                selected_products[component] = products[0]
                product_alternatives[component] = products[1:] if len(products) > 1 else []
    
    state["selected_products"] = selected_products
    state["product_alternatives"] = product_alternatives
    
    return state


def cart_composer_agent(state: CartPilotState) -> CartPilotState:
    """
    Agent 6: Cart Composer Agent
    Purpose: Compose final cart, validate completeness, calculate score
    Uses LLM: No (deterministic composition)
    """
    selected_products = state["selected_products"]
    required_components = state["required_components"]
    missing_deps = state["missing_dependencies"]
    compatibility_issues = state["compatibility_issues"]
    
    # Build final cart
    final_cart = []
    total_price = 0.0
    
    all_components = required_components + missing_deps
    
    for component in all_components:
        if component in selected_products:
            product = selected_products[component].copy()
            product["component"] = component
            final_cart.append(product)
            total_price += product.get("price", 0.0)
    
    # Calculate completeness score
    # Base score: all required components present
    required_present = sum(1 for comp in required_components if comp in selected_products)
    required_score = required_present / len(required_components) if required_components else 0.0
    
    # Dependency score: all dependencies satisfied
    deps_satisfied = sum(1 for dep in missing_deps if dep in selected_products)
    deps_score = 1.0 if not missing_deps else (deps_satisfied / len(missing_deps))
    
    # Compatibility score: no compatibility issues
    compat_score = 1.0 if not compatibility_issues else max(0.0, 1.0 - (len(compatibility_issues) * 0.1))
    
    completeness_score = (required_score * 0.5 + deps_score * 0.3 + compat_score * 0.2)
    
    # Generate summary
    cart_summary = f"Cart contains {len(final_cart)} items. Total: ${total_price:.2f}. "
    cart_summary += f"Completeness: {completeness_score:.1%}. "
    if compatibility_issues:
        cart_summary += f"Warning: {len(compatibility_issues)} compatibility issue(s)."
    
    # Validation errors
    validation_errors = []
    for comp in required_components:
        if comp not in selected_products:
            validation_errors.append(f"Missing required component: {comp}")
    
    for issue in compatibility_issues:
        validation_errors.append(f"Compatibility issue: {issue['component1']} <-> {issue['component2']}")
    
    state["final_cart"] = final_cart
    state["completeness_score"] = completeness_score
    state["cart_summary"] = cart_summary
    state["validation_errors"] = validation_errors
    
    return state

