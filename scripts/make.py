"""
Makes the README file <details> section.

    Usage:
        ``python scripts/make.py``

"""


def get_changes() -> list[str]:
    """
    Gets the changes from the changelog.md file.

    Output format
    -------------
        [version and message, first change, second change, ...]
    """
    with open("changelog.md", "r", encoding="utf-8") as f:
        changelog = f.readlines()
    changelog = [e.strip() for e in changelog]
    chg: list[str] = []
    for e in reversed(changelog):
        chg.append(e)
        if e[0] != "*":
            break
    return list(reversed(chg))


def update(chg: list[str]) -> None:
    """
    Updates README.md with changelog
    
    Parameters
    ----------
        chg : list[str]
            changelog extract
    """
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.readlines()
    index0: int = None
    index1: int = None
    for i, e in enumerate(readme):
        e.strip()
        if "<details>" in e:
            index0 = i
        elif "</details>" in e:
            index1 = i
    if index0 is None and index1 is None:
        raise ValueError(
            "Error [README make] : bad format, <details> tag not found")

    head = chg[0]
    head = head[4::].strip("*").replace("*", " :")

    details: list[str] = []
    details.append(f"    <summary> {head} (click to expand) </summary>")
    details.append("\n\n")
    for e in chg[1:]:
        details.append(f"{e}\n")
    details.append("\n")

    readme = readme[:index0 + 1] + details + readme[index1:]
    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(readme)


if __name__ == "__main__":
    # it just works
    update(get_changes())
