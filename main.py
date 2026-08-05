import subprocess
import time
import sys

KICK_CHANNEL = "Abo_Khrbaa"
YOUTUBE_STREAM_KEY = "7swd-bmce-ym7w-5e2m-499u"
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

def start_bridge():
    print(f"[*] Starting stable bridge for Kick channel: {KICK_CHANNEL}", flush=True)
    
    while True:
        p1 = None
        p2 = None
        try:
            # إضافة هيدرز متصفح حقيقي لـ streamlink لتجاوز الحظر الفوري
            streamlink_cmd = [
                "streamlink", 
                "--http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "--stdout", 
                f"https://kick.com/{KICK_CHANNEL}", 
                "best"
            ]
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-re",
                "-fflags", "+genpts+nobuffer",
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
            
            print("[*] Launching processes...", flush=True)
            p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen(ffmpeg_cmd, stdin=p1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            p1.stdout.close()
            
            # مهلة قصيرة للتأكد من استقرار البث وعدم حدوث حظر فوري
            time.sleep(5)
            
            print("[*] Stream bridge is running stable! Monitoring...", flush=True)
            
            while True:
                if p2.poll() is not None or p1.poll() is not None:
                    print("\n[!] Stream disconnected. Reconnecting...", flush=True)
                    break
                time.sleep(10)
                
        except Exception as e:
            print(f"\n[-] Error: {e}", flush=True)
            
        try:
            if p1: p1.kill()
            if p2: p2.kill()
        except:
            pass
            
        print("[!] Waiting 5 seconds before reconnecting...", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    start_bridge()
