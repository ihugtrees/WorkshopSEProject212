def create_filters(minimum, maximum, prating, category, srating):
    if not minimum:
        minimum = 0
    if not maximum:
        maximum = None
    else:
        maximum = float(maximum)
    if not prating:
        prating = 0
    if not srating:
        srating = 0
    return {"min": float(minimum), "max": maximum, "prating": float(prating), "category": category,
            "srating": float(srating)}
