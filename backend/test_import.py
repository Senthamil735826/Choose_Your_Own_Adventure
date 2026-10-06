import sys
import os
import types

current_dir = os.path.dirname(os.path.abspath(__file__))

if "backend" not in sys.modules:
    backend_mod = types.ModuleType("backend")
    backend_mod.__path__ = [current_dir]
    sys.modules["backend"] = backend_mod

# Now try importing
# pyrefly: ignore [missing-import]
from backend.core.config import settings
print(settings.API_PREFIX)
