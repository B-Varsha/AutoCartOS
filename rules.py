"""
Dependency and compatibility rules engine.
Deterministic rule-based logic for component relationships.
"""
from typing import Dict, List, Set, Tuple


# Component dependency rules: component -> required dependencies
DEPENDENCY_RULES: Dict[str, List[str]] = {
    "monitor": ["monitor_stand", "hdmi_cable"],
    "desktop_computer": ["monitor", "keyboard", "mouse", "power_cable"],
    "laptop": ["laptop_stand", "external_keyboard", "external_mouse"],
    "gaming_setup": ["gaming_monitor", "gaming_keyboard", "gaming_mouse", "gaming_headset"],
    "audio_setup": ["speakers", "audio_cable"],
    "webcam": ["usb_cable"],
    "printer": ["usb_cable", "printer_paper"],
    "router": ["ethernet_cable"],
    "external_storage": ["usb_cable"],
    "docking_station": ["usb_cable", "hdmi_cable"],
}

# Compatibility rules: (component1, component2) -> compatible
COMPATIBILITY_RULES: Dict[Tuple[str, str], bool] = {
    # Positive compatibilities
    ("macbook", "usb_c_adapter"): True,
    ("windows_laptop", "usb_c_adapter"): False,  # Windows laptops usually have USB-A
    ("gaming_monitor", "gaming_keyboard"): True,
    ("gaming_monitor", "gaming_mouse"): True,
    ("4k_monitor", "hdmi_2_1_cable"): True,
    ("1080p_monitor", "hdmi_2_1_cable"): True,  # Backward compatible
    ("wireless_keyboard", "wireless_mouse"): True,  # Can share USB receiver
    ("mechanical_keyboard", "gaming_setup"): True,
    
    # Incompatibilities
    ("macbook", "windows_keyboard"): False,  # Layout mismatch
    ("macbook", "windows_mouse"): False,
    ("mac_keyboard", "windows_laptop"): False,
    ("thunderbolt_dock", "usb_c_only_device"): False,
    ("vga_monitor", "hdmi_only_laptop"): False,
}

# Category-based compatibility
CATEGORY_COMPATIBILITY: Dict[str, Set[str]] = {
    "mac_ecosystem": {"macbook", "mac_keyboard", "mac_mouse", "thunderbolt_dock"},
    "windows_ecosystem": {"windows_laptop", "windows_keyboard", "windows_mouse", "usb_c_adapter"},
    "gaming_ecosystem": {"gaming_monitor", "gaming_keyboard", "gaming_mouse", "gaming_headset"},
}


def get_dependencies(component: str) -> List[str]:
    """Get required dependencies for a component."""
    return DEPENDENCY_RULES.get(component, [])


def check_compatibility(component1: str, component2: str) -> bool:
    """
    Check if two components are compatible.
    Returns True if compatible, False if incompatible, None if unknown.
    """
    # Direct rule check
    if (component1, component2) in COMPATIBILITY_RULES:
        return COMPATIBILITY_RULES[(component1, component2)]
    if (component2, component1) in COMPATIBILITY_RULES:
        return COMPATIBILITY_RULES[(component2, component1)]
    
    # Category-based check
    for category, components in CATEGORY_COMPATIBILITY.items():
        if component1 in components and component2 in components:
            return True
        if component1 in components and component2 not in components:
            # Cross-ecosystem might be incompatible
            for other_category, other_components in CATEGORY_COMPATIBILITY.items():
                if category != other_category and component2 in other_components:
                    # Check if there's explicit incompatibility
                    if (component1, component2) in COMPATIBILITY_RULES:
                        return COMPATIBILITY_RULES[(component1, component2)]
    
    # Default: assume compatible if no rule exists
    return True


def validate_component_set(components: List[str]) -> Tuple[List[str], List[Tuple[str, str, str]]]:
    """
    Validate a set of components for dependencies and compatibility.
    Returns: (missing_dependencies, compatibility_issues)
    """
    missing_deps = []
    compatibility_issues = []
    
    # Check dependencies
    all_required = set()
    for component in components:
        deps = get_dependencies(component)
        all_required.update(deps)
    
    missing_deps = [dep for dep in all_required if dep not in components]
    
    # Check compatibility
    for i, comp1 in enumerate(components):
        for comp2 in components[i+1:]:
            if not check_compatibility(comp1, comp2):
                compatibility_issues.append((comp1, comp2, "Incompatible components"))
    
    return missing_deps, compatibility_issues


def get_all_dependencies(components: List[str]) -> Dict[str, List[str]]:
    """Get all dependencies for a list of components."""
    result = {}
    for component in components:
        result[component] = get_dependencies(component)
    return result

