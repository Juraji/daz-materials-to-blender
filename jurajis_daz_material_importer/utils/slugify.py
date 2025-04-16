def slugify(*parts: str) -> str:
    result = []
    prev_was_underscore = False

    merged_parts = str.join('_', parts).lower()

    for c in merged_parts:
        if c.isalnum():
            result.append(c)
            prev_was_underscore = False
        else:
            if not prev_was_underscore:
                result.append("_")
                prev_was_underscore = True

    # Remove leading/trailing underscore if present
    if result and result[0] == "_":
        result = result[1:]
    if result and result[-1] == "_":
        result = result[:-1]

    return ''.join(result)
