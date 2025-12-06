from pathlib import Path
for item in Path.cwd().rglob("*.py"):
    print(item)
