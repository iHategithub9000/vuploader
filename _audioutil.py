import subprocess, os, json, base64, time

def check_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_to_wav(path, sample_rate):
	name = "tmp_" + str(int(time.time() * 1000))
	cmd = f"ffmpeg -f u8 -ar {sample_rate} -ac 1 -i \"{path}\" {name}.wav"
	subprocess.run(cmd, shell=True)
	return name + ".wav"

def get_sample_rate(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            path
        ],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    for stream in data["streams"]:
        if stream["codec_type"] == "audio":
            return int(stream["sample_rate"])

def shrink(path, target_bytes=10_000_000):
    size_bytes = os.path.getsize(path)
    sample_rate = get_sample_rate(path)
    channels = 1
    bytes_per_sample = 1 
    duration = size_bytes / (sample_rate * channels * bytes_per_sample)
    bitrate = (target_bytes * 8) / duration
    bitrate *= 0.9
    bitrate_kbps = max(6, min(int(bitrate / 1000), 128))
    output = "tmp_" + str(int(time.time() * 1000)) + ".opus"
    command = (
        f'ffmpeg '
        f'-i "{path}" '
        f'-c:a libopus -b:a {bitrate_kbps}k '
        f'"{output}"'
    )
    subprocess.run(command, shell=True)
    return output

