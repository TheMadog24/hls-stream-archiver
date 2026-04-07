def select_variant(variants, quality: str):
    if not variants:
        raise ValueError("No variants available")

    if quality == "best":
        selected = max(variants, key=lambda v: int(v.get("bandwidth", 0)))
        return selected, "best"

    for v in variants:
        if v.get("name") == quality:
            return v, f"name={quality}"

        resolution = v.get("resolution")
        if resolution:
            try:
                height = resolution.split("x")[1]
                if height == quality:
                    return v, f"resolution={resolution}"
            except IndexError:
                continue

    raise ValueError(f"Quality '{quality}' not found")