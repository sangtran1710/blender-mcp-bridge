import socket
import json
import sys
import time

HOST = 'localhost'
PORT = 9876

def send_script(script_path):
    try:
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        # Prepare command
        command = {
            "type": "execute_code",
            "params": {
                "code": script_content
            }
        }
        
        # Connect and send
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(60) 
            s.connect((HOST, PORT))
            
            # Send data
            s.sendall(json.dumps(command).encode('utf-8'))
            
            # Receive response
            data = b''
            start_time = time.time()
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    
                    # Try to parse JSON
                    try:
                        response = json.loads(data.decode('utf-8'))
                        return response # Success!
                    except json.JSONDecodeError:
                        # Continue reading
                        pass
                        
                    if time.time() - start_time > 10:
                        return {"status": "error", "message": "Timeout waiting for complete JSON"}
                        
                except socket.timeout:
                    break
            
            return {"status": "error", "message": " Connection closed without valid JSON"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <script_file>")
        sys.exit(1)
        
    script_file = sys.argv[1]
    print(f"Sending {script_file} to Blender...")
    result = send_script(script_file)
    print("Result:", json.dumps(result, indent=2))
