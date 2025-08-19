cd /d "D:\PythonProjects\ImageOptimizer"
"..\Python\python.exe" image_optimizer.py


# Interactive mode
"..\Python\python.exe" image_optimizer.py

# Direct compression
"..\Python\python.exe" image_optimizer.py photo.jpg -t 200 -f WEBP

# Batch process folder
"..\Python\python.exe" image_optimizer.py photos/ -b -t 150 -w 1920