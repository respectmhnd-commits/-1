import subprocess
import time

# إعدادات البث
KICK_CHANNEL = "Abo_Khrbaa"
YOUTUBE_STREAM_KEY = "7swd-bmce-ym7w-5e2m-499u"
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

def start_bridge():
    print(f"[*] جاري الاتصال ببث قناة Kick: {KICK_CHANNEL}...")
    
    # استخدام streamlink لجلب رابط البث المباشر من كيك بدقة عالية
    streamlink_cmd = ["streamlink", "--stdout", f"https://kick.com/{KICK_CHANNEL}", "best"]
    
    # استخدام ffmpeg لسحب البث وإعادة توجيهه إلى يوتيوب
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-i", "pipe:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        YOUTUBE_URL
    ]
    
    while True:
        try:
            print("[*] جارٍ تشغيل جسر البث المباشر...")
            p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen(ffmpeg_cmd, stdin=p1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            p1.stdout.close()
            p2.wait()
        except Exception as e:
            print(f"[-] حدث خطأ: {e}")
        
        print("[!] انقطع البث أو توقف، إعادة المحاولة خلال 5 ثوانٍ...")
        time.sleep(5)

if __name__ == "__main__":
    start_bridge()
 
