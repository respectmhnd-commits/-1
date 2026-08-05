import subprocess
import time
import sys

KICK_CHANNEL = "Abo_Khrbaa"
YOUTUBE_STREAM_KEY = "7swd-bmce-ym7w-5e2m-499u"
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

def start_bridge():
    print(f"[*] Starting unbreakable bridge for Kick channel: {KICK_CHANNEL}", flush=True)
    
    while True:
        p1 = None
        p2 = None
        try:
            # استخدام streamlink مع وسائط منع التوقف المؤقت
            streamlink_cmd = [
                "streamlink", 
                "--hds-live-edge", "2",
                "--hls-live-edge", "2",
                "--stdout", 
                f"https://kick.com/{KICK_CHANNEL}", 
                "best"
            ]
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-re",
                "-fflags", "+genpts+nobuffer",
                "-flags", "low_delay",
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
            
            print("[*] Launching stream processes...", flush=True)
            p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen(ffmpeg_cmd, stdin=p1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            p1.stdout.close()
            
            # مراقبة مستمرة، إذا توقف أي طرف يعيد الاتصال فورا
            while True:
                if p2.poll() is not None or p1.poll() is not None:
                    print("\n[!] Stream glitch detected. Reconnecting...", flush=True)
                    break
                time.sleep(2)
                
        except Exception as e:
            print(f"\n[-] Error: {e}", flush=True)
            
        try:
            if p1: p1.kill()
            if p2: p2.kill()
        except:
            pass
            
        print("[!] Restarting stream bridge instantly...", flush=True)
        time.sleep(2)

if __name__ == "__main__":
    start_bridge()
