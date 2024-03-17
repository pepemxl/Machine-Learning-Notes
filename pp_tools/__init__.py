"""
PYTHONPATH is set to the parent directory of the executed script. 
So if the executed script is inside a directory src, 
it will never be able to find the sister directory lib because it isn't within the path. 

There's a few choices;

- Just move lib/ into src/ if it belongs to your code. If it's an external package, it should be pip installed.
Have a top-level script outside of src/ that imports and runs src.main. This will add the top-level directory to python path.
In src/main.py modify sys.path to include the top-level directory. This is usually frowned upon.
Invoke src/main.py as a module with python -m src.main which will add the top-level directory to the python path. Kind of annoying to type, plus you'll need to change all your imports.
"""