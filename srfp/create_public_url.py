from pyngrok import ngrok
import time

print("🚀 Creating public URL for your KPI application...")
print("This will allow you to access the app from anywhere!")

# Create public URL
public_url = ngrok.connect(5000)
print(f"\n✅ Your application is now accessible at:")
print(f"🌐 {public_url}")
print(f"\n📱 You can now access it from your mobile phone!")
print(f"🔗 Share this URL with anyone to show your application")

print(f"\n⏰ This URL will be active as long as this script runs")
print(f"🛑 Press Ctrl+C to stop the public URL")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(f"\n🛑 Stopping public URL...")
    ngrok.kill()
    print(f"✅ Public URL stopped")
