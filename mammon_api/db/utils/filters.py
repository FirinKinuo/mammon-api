def leave_required_keys(filter_dict: dict, required_keys: list) -> dict:
    """
    Get a dictionary filtered by the necessary keys
    Args:
        filter_dict (dict): Dictionary to be filtered
        required_keys (list): List of required keys

    Returns:
        dict: Filtered dictionary
    """
    return {key: value for key, value in filter_dict.items() if key in required_keys}
