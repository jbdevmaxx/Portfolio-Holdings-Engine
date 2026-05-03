from pathlib import Path


def ensure_directory(directory: Path) -> None:
    # Ensure directory exists, if not create it

    directory.mkdir(parents=True, exist_ok=True)

def write_text_file(file_path: Path, content: str) -> None:
    # rite text content to a file using UTF-8 encoding and create parent folder if needed

    ensure_directory(file_path.parent)
    file_path.write_text(content, encoding="utf-8")

def safe_write_file(file_path: Path, content: str) -> None:
    # Writes a file only if it does not already exist to prevent overwriting uuser-edited reesearch notes or reports

    ensure_directory(file_path.parent)

    if file_path.exists():
        print(f"Skipped existing file: {file_path}")
        return
    
    write_text_file(file_path, content)
    print(f"Created file: {file_path}")
    
    
    



def safe_write_file(file_path: Path, content: str) -> None:
    # Safely writes content to a file if it does not exist, o
    if file_path.exists():
        print(f"Skipped existing file: {file_path}")
        return
    
    file_path.write_text(content, encoding="utf-8")
    print(f"Created file: {file_path}")
