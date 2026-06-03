import pkgutil
import importlib

blueprints = []

for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")

    if hasattr(module, "bp"):
        blueprints.append(module.bp)
        
# from .user_controller import user_bp
# from .product_controller import product_bp

# blueprints = [
#     user_bp,
#     product_bp
# ]