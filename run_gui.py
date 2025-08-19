import sys
import os

# Add portable Python to path
python_path = os.path.join(os.path.dirname(__file__), '..', 'Python')
sys.path.insert(0, python_path)

# Import and run the GUI version
if __name__ == "__main__":
    import image_optimizer_gui