from datetime import datetime

def do_cron():
    with open("app/cron.log", "rt") as filein:
        text = filein.read()
        text += f"\n{datetime.utcnow().strftime('%Y-%m%dT%H:%M:%SZ')}"
        
    with open("app/cron.log", "wt") as fileout:
        fileout.write(text)



if __name__ == "__main__":
    do_cron()