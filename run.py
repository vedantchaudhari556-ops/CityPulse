"""
CityPulse - Smart City Emergency Response & Live Traffic Management
===================================================================
Application Launcher
Starts the backend Flask server hosting both the RESTful/SSE API
and the interactive web dashboard.

Usage:
    python run.py
"""

import os
import sys

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 75)
    print("                      CITYPULSE SMART CITY PLATFORM")
    print("        Emergency Response, Incident Coordination & Traffic Management")
    print("=" * 75)
    print(f" * Target City:  Nagpur, Maharashtra, India (21.1458° N, 79.0882° E)")
    print(f" * Dashboard:    http://localhost:{port}")
    print(f" * System Info:  http://localhost:{port}/api/system/status")
    print(f" * Admin Portal: Username: admin | Password: citypulse2026")
    print("-" * 75)
    print(" * Live Map:     OpenStreetMap & Leaflet.js (Over internet)")
    print(" * Routing:      OSRM Open Source Routing Machine")
    print(" * Real-time:    Server-Sent Events (SSE)")
    print("=" * 75)

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
