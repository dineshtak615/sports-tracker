import os
from google.colab import files

if os.path.exists("/content/output_tracked.mp4"):
    print("✅ Downloading your video...")
    files.download("/content/output_tracked.mp4")
else:
    print("❌ Output not found - Cell 4 did not finish!")
