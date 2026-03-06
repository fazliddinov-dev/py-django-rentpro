def generate_version_keys(model_name: str):
    """
    Automatically generate Redis version keys for list and detail caches
    based on the model name.

    Example:
        generate_version_keys("SubscriptionProducts")
        -> ("subscriptionproducts:list_version", "subscriptionproducts:detail_version")
    """
    model_key = model_name.lower()
    list_key = f"{model_key}:list_version"
    detail_key = f"{model_key}:detail_version"
    return list_key, detail_key
