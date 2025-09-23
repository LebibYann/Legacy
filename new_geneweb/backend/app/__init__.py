"""Application package root.

Having this file ensures mypy treats the directory as a regular package
so that modules like `settings` are only discovered as `app.settings`
and not also as a top-level `settings` module.
"""

__all__ = [
    "main",
]
