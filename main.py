import subprocess
import time
import sys

KICK_CHANNEL = "Abo_Khrbaa"
YOUTUBE_STREAM_KEY = "7swd-bmce-ym7w-5e2m-499u"
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

def start_bridge():
    print(f"[*] Starting robust streaming bridge for Kick channel: {KICK_CHANNEL}", flush=True)
    
    while True:
        p1 = None
        p2 = None
        try:
            streamlink_cmd = ["streamlink", "--stdout", f"https://kick.com/{KICK_CHANNEL}", "best"]
            
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
            
            print("[*] Launching Streamlink & FFmpeg processes...", flush=True)
            p1 = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen(ffmpeg_cmd, stdin=p1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            p1.stdout.close()
            
            print("[*] Stream is LIVE! Monitoring process...", flush=True)
            
            while True:
                retcode = p2.poll()
                if retcode is not None:
                    print(f"\n[!] Warning: FFmpeg process exited with code {retcode}.", flush=True)
                    break
                
                # فحص ما إذا كان streamlink قد توقف أيضاً
                if p1.poll() is not None:
                    print(f"\n[!] Warning: Streamlink process stopped.", flush=True)
                    break
                
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(5)
                
        except Exception as e:
            print(f"\n[-] Exception caught in bridge loop: {e}", flush=True)
            
        try:
            if p1: p1.kill()
            if p2: p2.kill()
        except:
            pass
            
        print("\n[!] Re-establishing connection to YouTube in 3 seconds...", flush=True)
        time.sleep(3)

if __name__ == "__main__":
    start_bridge()

