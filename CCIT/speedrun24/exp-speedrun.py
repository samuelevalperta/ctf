import subprocess
import time

# Define the function to measure the response time
def measure_time(guess):
    # Start the Rust program as a subprocess
    proc = subprocess.Popen(['./speedrun'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Record the start time
    start_time = time.time()

    # Send the guess to the Rust program
    proc.stdin.write(guess.encode() + b'\n')
    proc.stdin.flush()

    # Wait for the process to complete and capture the output
    output, _ = proc.communicate()

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    return elapsed_time, output.decode()

# Main function to perform the timing attack
def timing_attack():
    flag = ""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}"
    
    for position in range(1, 50):  # Adjust the range based on the expected flag length
        timings = []
        for char in charset:
            guess = flag + char
            elapsed_time, output = measure_time(guess)
            timings.append((elapsed_time, char, output.strip()))

        # Find the character with the maximum elapsed time
        timings.sort(reverse=True)
        best_char = timings[0][1]
        flag += best_char

        print(f"Position {position}: Best guess so far is '{flag}'")
        print(f"Debug: {timings[0]}")

        # Check if the current guess is correct
        if "Correct!" in timings[0][2]:
            break

    print(f"Flag found: {flag}")

# Run the timing attack
if __name__ == "__main__":
    timing_attack()

