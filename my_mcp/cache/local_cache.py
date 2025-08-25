import pickle
import functools
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar, cast

from my_mcp.config.config_manager import ConfigManager

T = TypeVar('T')


def local_cache(max_age_days: int = 1):
    """
    Decorator that caches the result of a function on disk.
    
    The decorated function's return value must have serialize() and deserialize() methods.
    serialize() must return bytes that can be saved as a zip file.
    
    Args:
        max_age_days: Number of days to keep the cache valid
        
    Returns:
        Decorated function that uses disk caching
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Get cache directory from ConfigManager
            cache_dir = Path(ConfigManager().cache)
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Create a cache key based on function name and arguments
            cache_key = f"{func.__module__}.{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
            data_path = cache_dir / f"{cache_key}.zip"
            meta_path = cache_dir / f"{cache_key}.meta"
            
            # Check if cache file exists and is valid
            if data_path.exists() and meta_path.exists():
                with open(meta_path, 'rb') as f:
                    metadata = pickle.load(f)
                    created_time = metadata.get('created_time')
                    result_class = metadata.get('result_class')
                    
                    # Check if cache is still valid
                    if created_time and datetime.now() < created_time + timedelta(days=max_age_days):
                        # Use the deserialize method to get the cached result
                        if not result_class or not hasattr(result_class, 'deserialize'):
                            raise AttributeError(f"Cached result from {func.__name__} must have a 'deserialize' class method")
                        
                        with open(data_path, 'rb') as data_file:
                            serialized_data = data_file.read()
                            return cast(T, result_class.deserialize(serialized_data))
            
            # Execute the function if cache is invalid or doesn't exist
            result = func(*args, **kwargs)
            
            # Check if result has a serialize method
            if not hasattr(result, 'serialize'):
                raise AttributeError(f"Return value from {func.__name__} must have a 'serialize' method")
            
            # Get serialized bytes from the result
            serialized_bytes = result.serialize()
            if not isinstance(serialized_bytes, bytes):
                raise TypeError(f"serialize() method of {result.__class__.__name__} must return bytes")
            
            # Save the serialized data directly as a zip file
            with open(data_path, 'wb') as data_file:
                data_file.write(serialized_bytes)
            
            # Save metadata separately
            metadata = {
                'created_time': datetime.now(),
                'result_class': result.__class__
            }
            
            with open(meta_path, 'wb') as meta_file:
                pickle.dump(metadata, meta_file)
                
            return result
        
        return wrapper
    
    return decorator