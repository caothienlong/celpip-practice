# 🌐 Local Network Hosting Guide

## Quick Start - Share on Local Network

### 1. Run Flask with Network Access

Instead of the default `python app.py`, run with host binding:

```bash
python app.py --host 0.0.0.0
```

Or modify `app.py` to always allow network access:

```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True
    )
```

---

## 2. Find Your Local IP Address

### On macOS/Linux:
```bash
# Method 1: Using ifconfig
ifconfig | grep "inet " | grep -v 127.0.0.1

# Method 2: Using hostname
hostname -I

# Method 3: Using ip (Linux)
ip addr show | grep "inet " | grep -v 127.0.0.1
```

Your local IP will look like:
- `192.168.1.XXX` (most common)
- `10.0.0.XXX` (some routers)
- `172.16.XXX.XXX` (less common)

### On Windows:
```cmd
ipconfig
```

Look for "IPv4 Address" under your active network adapter.

---

## 3. Access from Other Devices

Once the server is running, other devices on the **same Wi-Fi network** can access it at:

```
http://YOUR_LOCAL_IP:5000
```

**Example:**
If your IP is `192.168.1.100`:
```
http://192.168.1.100:5000
```

---

## Step-by-Step Example

### Host Machine (Running Flask):

```bash
# 1. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 2. Find your IP
ifconfig | grep "inet " | grep -v 127.0.0.1
# Output: inet 192.168.1.100 netmask ...

# 3. Start server with network access
python app.py --host 0.0.0.0

# Output:
# * Running on http://127.0.0.1:5000
# * Running on http://192.168.1.100:5000  ← Use this!
```

### Client Devices (Phone, Tablet, Other Computer):

1. Connect to **same Wi-Fi network**
2. Open browser
3. Go to: `http://192.168.1.100:5000`
4. Start practicing!

---

## Permanent Configuration

### Option 1: Modify app.py

```python
# At the bottom of app.py
if __name__ == '__main__':
    import os
    
    # Get host from environment or default to 0.0.0.0
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    app.run(
        host=host,
        port=port,
        debug=True
    )
```

Then run normally:
```bash
python app.py
```

### Option 2: Use Flask Environment Variables

```bash
# Set environment variables
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000

# Run with flask command
flask run
```

### Option 3: Create Run Script

**`run_network.sh` (macOS/Linux):**
```bash
#!/bin/bash
source venv/bin/activate
python app.py --host 0.0.0.0 --port 5000
```

Make executable:
```bash
chmod +x run_network.sh
./run_network.sh
```

**`run_network.bat` (Windows):**
```batch
@echo off
call venv\Scripts\activate
python app.py --host 0.0.0.0 --port 5000
```

Run:
```cmd
run_network.bat
```

---

## Testing from Different Devices

### From Your Computer (Host):
- `http://localhost:5000` ✅
- `http://127.0.0.1:5000` ✅
- `http://192.168.1.100:5000` ✅

### From Phone/Tablet:
- `http://192.168.1.100:5000` ✅

### From Another Computer:
- `http://192.168.1.100:5000` ✅

---

## Troubleshooting

### Issue 1: Cannot Connect from Other Devices

**Check Firewall:**

**macOS:**
```bash
# Allow Python through firewall
System Preferences → Security & Privacy → Firewall → Firewall Options
→ Allow incoming connections for Python
```

**Linux:**
```bash
# Allow port 5000
sudo ufw allow 5000
```

**Windows:**
```powershell
# Allow port 5000
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=TCP localport=5000
```

### Issue 2: Wrong IP Address

Make sure you're using the **Wi-Fi IP**, not:
- ❌ `127.0.0.1` (localhost only)
- ❌ `0.0.0.0` (binding address, not accessible)
- ❌ Ethernet IP (if connected via Wi-Fi)

### Issue 3: Different Networks

Both devices must be on the **same network**:
- Same Wi-Fi name
- Not using VPN on either device
- Not on guest network

### Issue 4: IP Address Changed

If you disconnect/reconnect to Wi-Fi, your IP might change:
```bash
# Check current IP
ifconfig | grep "inet " | grep -v 127.0.0.1
```

---

## Advanced: Port Forwarding (Internet Access)

⚠️ **Security Warning**: This exposes your app to the internet!

### For Development Only:

1. **Use ngrok** (easiest):
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Create tunnel
ngrok http 5000

# Output:
# Forwarding https://abc123.ngrok.io -> http://localhost:5000
```

2. **Share the URL**:
```
https://abc123.ngrok.io
```

Anyone with this URL can access your app!

### For Production:

Consider:
- **Heroku**: Easy deployment
- **PythonAnywhere**: Free tier available
- **DigitalOcean**: Full control
- **AWS/Google Cloud**: Enterprise solutions

---

## Security Considerations

### For Local Network Sharing:

✅ **Safe:**
- Sharing on home Wi-Fi with trusted devices
- Testing on your own phone/tablet
- Short-term development testing

⚠️ **Be Careful:**
- Public Wi-Fi (coffee shop, library)
- Office networks (might violate policy)
- Leaving server running unattended

❌ **Never:**
- Expose to internet without proper security
- Use on untrusted networks
- Store real user data without encryption

### Production Checklist:

Before deploying publicly:
- [ ] Turn off `debug=True`
- [ ] Use proper WSGI server (gunicorn, waitress)
- [ ] Set up HTTPS/SSL
- [ ] Use environment variables for secrets
- [ ] Implement authentication
- [ ] Set up database (instead of JSON files)
- [ ] Add rate limiting
- [ ] Enable CORS properly
- [ ] Set up logging and monitoring

---

## Quick Reference

### Start Server (Network Access):
```bash
python app.py --host 0.0.0.0
```

### Find IP:
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

### Access URL:
```
http://YOUR_IP:5000
```

### Test:
```bash
# From host machine
curl http://localhost:5000

# From other device (replace with your IP)
curl http://192.168.1.100:5000
```

---

## Example Session

```bash
$ source venv/bin/activate
(venv) $ ifconfig | grep "inet " | grep -v 127.0.0.1
        inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255

(venv) $ python app.py --host 0.0.0.0
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000  ← Share this URL!
Press CTRL+C to quit
```

**On your phone/tablet:**
1. Connect to same Wi-Fi
2. Open browser
3. Go to: `http://192.168.1.100:5000`
4. Done! 🎉

---

## Tips

1. **Bookmark the IP** on mobile devices for quick access
2. **Use QR Code** to share the URL:
   ```bash
   # Generate QR code (install qrencode)
   echo "http://192.168.1.100:5000" | qrencode -t UTF8
   ```

3. **Static IP** (optional): Configure router to always assign same IP to your computer

4. **Multiple Ports**: Run multiple Flask apps on different ports:
   ```bash
   python app.py --host 0.0.0.0 --port 5000  # App 1
   python app2.py --host 0.0.0.0 --port 5001  # App 2
   ```

---

## Summary

| Method | Command | Access From |
|--------|---------|-------------|
| Localhost only | `python app.py` | Host computer only |
| Local network | `python app.py --host 0.0.0.0` | Same Wi-Fi devices |
| Internet (dev) | `ngrok http 5000` | Anywhere |

---

**Need Help?**
- Firewall issues → Check OS firewall settings
- Can't find IP → Use multiple methods to find IP
- Connection refused → Check Flask is running on 0.0.0.0
- Different network → Ensure same Wi-Fi

---

*Last Updated: December 2025*

