import subprocess
import time
import sys

KICK_CHANNEL = "ABO8ALYY"
YOUTUBE_STREAM_KEY = "7swd-bmce-ym7w-5e2m-499u"
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

def start_bridge():
    print(f"[*] Starting anti-403 bridge for Kick channel: {KICK_CHANNEL}", flush=True)
    
    # استخدام yt-dlp مع تفعيل محاكاة المتصفح بالكامل لتجاوز الحظر
    ytdlp_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-check-certificates",
        "--geo-bypass",
        "--extractor-args", "kick:impersonate=True",
        "--get-url",
        f"https://kick.com/{KICK_CHANNEL}"
    ]
    
    while True:
        p2 = None
        try:
            print("[*] Fetching secure stream URL...", flush=True)
            direct_url = subprocess.check_output(ytdlp_cmd, universal_newlines=True).strip()
            
            if not direct_url or "http" not in direct_url:
                print("[!] Stream URL not found or channel offline. Retrying in 10 seconds...", flush=True)
                time.sleep(10)
                continue

            print("[*] Secure URL acquired! Launching FFmpeg...", flush=True)
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-re",
                "-fflags", "+genpts+nobuffer",
                "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "-i", direct_url,
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
            
            p2 = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            while True:
                retcode = p2.poll()
                if retcode is not None:
                    print(f"\n[!] FFmpeg ended with code {retcode}. Refreshing...", flush=True)
                    break
                time.sleep(10)
                
        except Exception as e:
            print(f"\n[-] Error: {e}", flush=True)
            
        try:
            if p2: p2.kill()
        except:
            pass
            
        print("[!] Re-checking in 5 seconds...", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    start_bridge()
