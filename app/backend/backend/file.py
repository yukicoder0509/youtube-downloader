import os

def scan_dir(path: str, depth: int | None = None, include_file: bool = False) -> dict[str, str | list]:
    node = {
        "name": os.path.basename(path) or "root",
        "type": "directory",
        "children": []
    }

    if depth is not None and depth <= 0:
        return node

    try:
        for entry in os.scandir(path):
            if entry.name.startswith('.'):
                continue # Ignore hidden files and directories
            if entry.is_dir(follow_symlinks=False):
                node["children"].append(scan_dir(entry.path, depth=depth-1 if depth is not None else None))
            elif include_file and entry.is_file(follow_symlinks=False):
                node["children"].append({
                    "name": entry.name,
                    "type": "file",
                    "size": entry.stat().st_size
                })
    except PermissionError:
        pass  # Skip directories/files we can't access
    return node