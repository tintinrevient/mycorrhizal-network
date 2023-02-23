import subprocess
from dataclasses import dataclass


@dataclass
class Hop(object):
    url: str
    ip: str
    elapse: float


def traceroute(hostname):

    traceroute = subprocess.Popen(["traceroute", hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    hop_list = []
    for line in iter(traceroute.stdout.readline, b""):
        line = line.decode("utf-8")

        segments = line.split("  ")
        matches = ["(", ")"]
        if len(segments) > 2 and all([x in segments[1] for x in matches]) and "ms" in segments[2]:
            url = segments[1][0: segments[1].index("(")].strip()
            ip = segments[1][segments[1].index("(")+1: segments[1].index(")")]
            elapse = float(segments[2][0: segments[2].index("ms")].strip())

            hop = Hop(url=url, ip=ip, elapse=elapse)
            hop_list.append(hop)

    return hop_list


if __name__ == "__main__":
    hop_list = traceroute("google.com")
    print(hop_list)
