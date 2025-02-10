from importlib.metadata import requires
from typing import Union


def is_installed_with(extra: Union[str, list[str]]) -> bool:
    """Check if anonipy was installed with specific optional dependencies.

    Args:
        extra: The optional dependency or list of dependencies to check.
            Valid values are: 'dev', 'test', 'quant', 'all'

    Returns:
        True if package was installed with the specified optional dependencies,
            False otherwise.

    Example:
        >>> from anonipy.utils.package import is_installed_with
        >>> is_installed_with('dev')  # check if dev dependencies are installed
        >>> is_installed_with(['dev', 'test'])  # check multiple dependency groups
    """
    if isinstance(extra, str):
        extra = [extra]

    try:
        package_requires = requires("anonipy") or []
        installed_extras = set()

        for req in package_requires:
            if "extra == " in req:
                installed_extras.add(req.split("extra == ")[1].strip("\"'"))

        return any(e in installed_extras for e in extra)
    except Exception:
        return False
