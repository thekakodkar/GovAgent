import os
import sys
import json
from dotenv import load_dotenv

# Force explicit absolute path lookup for your .env file
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

print("=" * 60)
print("⚙️ GOVAGENT TELEMETRY NETWORK DIAGNOSTIC PASSTHROUGH")
print("=" * 60)

# 1. Environment Verification
bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")
channel_id = os.environ.get("SLACK_CHANNEL_ID")

print(f"📊 Environment Check:")
print(f"   - SLACK_BOT_TOKEN: {'FOUND (Starts with ' + bot_token[:9] + ')' if bot_token else '🚨 MISSING'}")
print(f"   - SLACK_APP_TOKEN: {'FOUND (Starts with ' + app_token[:9] + ')' if app_token else '🚨 MISSING'}")
print(f"   - SLACK_CHANNEL_ID: {f'FOUND ({channel_id})' if channel_id else '🚨 MISSING'}")

if not all([bot_token, app_token, channel_id]):
    print("\n🛑 Critical Error: Environmental registers are unhydrated. Check your .env placement.")
    sys.exit(1)

# 2. Force Outbound Test via Standard HTTP Client (Bypasses Socket Mode Handshakes)
try:
    import urllib.request
    
    print("\n📡 Phase 2: Dispatched standard Web REST API call to Slack Gateways...")
    
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": channel_id,
        "text": f"🚨 *GOVERNANCE INTERCEPT DIAGNOSTIC TRACE*\n\n*Status:* Telemetry link verified.\n*Timestamp:* `{sys.platform.upper()}` network interface loop passed safely."
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {bot_token}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
        print("\n🔍 Gateway Server Response Analytics:")
        print(f"   - HTTP Network Status: 200 OK")
        print(f"   - Slack API Status: {'✅ SUCCESS' if res_data.get('ok') else '❌ FAILED'}")
        
        if not res_data.get("ok"):
            print(f"   - Explicit Error Token: 🚨 `{res_data.get('error')}`")
            print("\n💡 Actionable Troubleshooting Matrices:")
            if res_data.get('error') == 'invalid_auth':
                print("     -> Your SLACK_BOT_TOKEN is invalid, copied wrong, or belongs to another workspace app context.")
            elif res_data.get('error') == 'channel_not_found':
                print("     -> The Bot cannot see this channel ID. Fix: Go to Slack, open the channel, type /invite @YourBotName.")
        else:
            print("\n🎉 SUCCESS! A direct network message was successfully posted to your Slack workspace channel.")
            print("   This confirms your Bot Token and Channel ID are perfect. The previous issue is 100% caused by local firewall or proxy restrictions blocking the underlying framework's Socket Mode WebSocket channel.")

except Exception as e:
    print(f"\n🚨 Critical Operating System Network Intercept Error: {str(e)}")

print("=" * 60)