export async function getAvailableDirectories(
  depth = 2,
  root = false,
  relative = true
) {
  const data = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/scan${depth ? `?depth=${depth}` : ""}`
  );
  const directories = await data.json();

  // Recursively collect all directory paths
  function collectDirs(node, currentPath = "") {
    let dirs = [];
    if (node.type === "directory") {
      const path = currentPath ? `${currentPath}/${node.name}` : node.name;
      dirs.push(path);
      if (Array.isArray(node.children)) {
        node.children.forEach((child) => {
          dirs = dirs.concat(collectDirs(child, path));
        });
      }
    }
    return dirs;
  }

  const allDirs = collectDirs(directories);
  const resultDirs = root ? allDirs : allDirs.slice(1);

  // Convert to relative paths if requested
  if (relative && resultDirs.length > 0) {
    const base = allDirs[0];
    return resultDirs.map((dir) => {
      if (dir == base) return ".";
      return dir.replace(new RegExp(`^${base}/?`), "");
    });
  }
  return resultDirs;
}

export async function downloadMedia(url, type, directory) {
  const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, type, dir: directory }),
  });
  return response.json();
}
