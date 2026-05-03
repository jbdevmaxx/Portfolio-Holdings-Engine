def join_lines(lines: list[str]) -> str:
    #Join a list of strings into Markdown-friendly newline-separated text.
    
    return "\n".join(str(line) for line in lines)


def bullet_list(items: list[str]) -> str:
   # Convert a list of plain strings into a Markdown bullet list.
    if not items:
        return "- None"

    return "\n".join(f"- {item}" for item in items)


def markdown_section(title: str, content: str, level: int = 2) -> str:
    
    # Create a Markdown section with a heading and body content.

    heading = "#" * level
    return f"{heading} {title}\n\n{content.strip()}\n"