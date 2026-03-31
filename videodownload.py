!pip install -q yt-dlp
!yt-dlp -f "best[ext=mp4][height<=480]" \
        -o "/content/input_video.mp4" \
        "https://www.youtube.com/watch?v=hGmAPvLuBOQ"

import os
if os.path.exists("/content/input_video.mp4"):
    size = os.path.getsize("/content/input_video.mp4")
    print(f"✅ Video ready! Size: {size/1024/1024:.1f} MB")
else:
    print("❌ Download failed!")
