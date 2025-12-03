import os
import sys
import select

FIFO_A_TO_B = "/tmp/fifo_a_to_b1"
FIFO_B_TO_A = "/tmp/fifo_b_to_a1"

def ensure_fifo(path):
    """Create the FIFO if it does not exist."""
    if not os.path.exists(path):
        print(f"[INFO] Creating FIFO: {path}")
        os.mkfifo(path)

def setup_fifos():
    """Ensure both FIFOs exist."""
    ensure_fifo(FIFO_A_TO_B)
    ensure_fifo(FIFO_B_TO_A)

def main():
    

    

    # Ensure pipes exist
    setup_fifos()

    # Assign read/write pipes based on role
    
   
    READ_FIFO = FIFO_A_TO_B
    WRITE_FIFO = FIFO_B_TO_A

    
    print(f"[INFO] Reading from: {READ_FIFO}")
    print(f"[INFO] Writing to:   {WRITE_FIFO}")

    # Open reading end (non-blocking)
    read_fd = os.open(READ_FIFO, os.O_RDONLY | os.O_NONBLOCK)

    # Open writing end (non-blocking)
    # O_WRONLY blocks if the other side hasn't opened the read end yet
    # So we try until it succeeds
    while True:
        try:
            write_fd = os.open(WRITE_FIFO, os.O_WRONLY | os.O_NONBLOCK)
            break
        except OSError:
            print("[INFO] Waiting for the other side to connect...")
            import time
            time.sleep(0.5)

    print("[INFO] Connected! Start typing...")

    while True:
        readable, _, _ = select.select([read_fd, sys.stdin], [], [])

        # Incoming message
        if read_fd in readable:
            data = os.read(read_fd, 4096)
            if data:
                print(f"\nFrom other: {data.decode().strip()}")
            else:
                print("[INFO] Other side closed the pipe.")
                break

        # Outgoing message
        if sys.stdin in readable:
            msg = sys.stdin.readline().strip()
            if msg:
                os.write(write_fd, msg.encode() + b"\n")

if __name__ == "__main__":
    main()
