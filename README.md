# CityPulse — Smart City Emergency Response & Live Traffic Management

> **Operational Geospatial Platform for Urban Incident Coordination, Hospital Discovery, and Real Road Routing**  
> *Target City: Nagpur, Maharashtra, India (`21.1458° N, 79.0882° E`)*

---

## 1. Problem Statement & Executive Summary

Modern urban areas face compounding crises: traffic gridlock, recurring road accidents, delayed emergency service dispatch, and fragmented coordination between citizens and municipal authorities. 

**CityPulse** is a complete, production-ready full-stack web application designed for municipal emergency command centers and citizen reporting. It addresses these challenges by integrating:
1. **A Real Interactive Geospatial Map**: Full street-level zoom, pan, and dragging powered by **Leaflet.js and OpenStreetMap**, loaded live over the internet.
2. **Citizen Incident Reporting**: Real-time reporting with geographic coordinate picking, reverse-geocoding, photographic scene uploads, and Server-Sent Events (SSE) live synchronization.
3. **Emergency Hospital Discovery**: Geographic discovery of emergency medical facilities in Nagpur queried via the **OpenStreetMap Overpass API** with localized resilience caching.
4. **Road Routing & Route Assistance**: Genuine road network routing powered by the **Open Source Routing Machine (OSRM)**, providing accurate road distances (km), estimated driving travel times (min), step maneuvers, and direct external navigation links (Google Maps / OpenStreetMap).
5. **Role-Based Incident Lifecycle Tracking**: Authorized dispatchers can verify reports, assign emergency units (`Reported` $\to$ `Verified` $\to$ `Responding` $\to$ `Resolved`), log dispatch call signs, and clear cleared hazards.
6. **Data Integrity & Live Traffic Transparency**: OpenStreetMap tiles and OSRM routes are 100% free and real. Traffic flow requires a documented TomTom API key in `.env`; if unconfigured, it is honestly labeled rather than displaying misleading synthetic traffic.

---

## 2. Architecture & Technology Stack

```
   ┌──────────────────────────────────────────────────────────────┐
   │                      FRONTEND LAYER                          │
   │  Leaflet.js (v1.9.4) • OpenStreetMap Tiles • Chart.js        │
   │  Lucide Icons • Single Page Responsive Dashboard (HTML/CSS/JS)│
   └──────────────────────────────▲───────────────────────────────┘
                                  │ REST / SSE
   ┌──────────────────────────────▼───────────────────────────────┐
   │                      BACKEND LAYER                           │
   │  Python Flask Server • Threaded SSE Event Broadcaster        │
   │  Werkzeug PBKDF2 Password Hashing • Nominatim Geocoding Proxy │
   │  OSRM Routing Engine Proxy • Secure TomTom Flow Tile Proxy    │
   └──────────────────────────────▲───────────────────────────────┘
                                  │ Parameterized SQL
   ┌──────────────────────────────▼───────────────────────────────┐
   │                     PERSISTENCE LAYER                        │
   │  SQLite (citypulse.db) with WAL Mode & B-Tree Spatial Indexes │
   │  Structured for PostgreSQL / PostGIS Schema Portability      │
   └──────────────────────────────────────────────────────────────┘
```

- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3 with custom Dark Navy/Charcoal operations theme (`#080c14`, `#0f172a`, `#1e293b`) and Cyan/Alert accents (`#06b6d4`, `#ef4444`).
- **Mapping Engine**: Leaflet.js v1.9.4 consuming OpenStreetMap Standard and CartoDB Dark Matter raster tiles.
- **Backend API**: Python 3.10+ with Flask 3.x, Flask-CORS, and Server-Sent Events.
- **Routing Engine**: Project OSRM (Open Source Routing Machine) driving profile.
- **Geocoding**: OpenStreetMap Nominatim reverse and forward geocoding.
- **POIs & Hospitals**: OpenStreetMap Overpass API with local SQLite cache.
- **Persistence**: SQLite with WAL (Write-Ahead Logging), indexed foreign keys, and audit logging.

---

## 3. Real Data vs. External API Key Boundaries

In strict compliance with smart-city integrity requirements:

| Capability | Provider | Status | API Key Required? | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Interactive City Map** | OpenStreetMap / Leaflet.js | **100% Live & Free** | ❌ No | Real street-level tiles loaded over the web |
| **Road Routing & Travel Times** | Project OSRM | **100% Live & Free** | ❌ No | Actual road network geometry & turn-by-turn steps |
| **Hospital Discovery** | OSM Overpass API & Nagpur Cache | **100% Live & Free** | ❌ No | Verified hospitals (AIIMS, GMCH, Kingsway, etc.) |
| **Incident Reporting & Sync** | Flask Backend & SSE | **100% Live & Free** | ❌ No | Persisted in SQLite with immediate broadcast |
| **Forward & Reverse Geocoding** | OSM Nominatim | **100% Live & Free** | ❌ No | Street address lookup & coordinate resolution |
| **Live Traffic Congestion Flow** | TomTom Traffic Flow API | Configurable | 🔑 **Yes** (`TOMTOM_API_KEY`) | Free tier (2,500 req/day). Clearly labeled if omitted |
| **Emergency Vehicle GPS (CAD/AVL)** | Municipal Telematics | Hardware Dependent | N/A | Strictly not faked; labeled as awaiting CAD feed |

---

## 4. Quickstart Guide

### Prerequisites
- Python 3.10 or higher
- Internet access (for OSM map tiles, OSRM road routing, and Nominatim search)

### Step 1: Clone or Navigate to Directory
```bash
cd c:\Users\SONY\Desktop\Crisis-Before-Crisis
```

### Step 2: Install Dependencies
```bash
pip install -r backend/requirements.txt
```
*(Dependencies: `flask`, `flask-cors`, `python-dotenv`, `requests`, `truststore`, `werkzeug`)*

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optionally set `TOMTOM_API_KEY=your_key` if you have a TomTom developer account).*

### Step 4: Launch CityPulse
```bash
python run.py
```

### Step 5: Open in Browser
Visit: **[http://localhost:8000](http://localhost:8000)**

---

## 5. Default Credentials & User Roles

| Role | Username | Password | Privileges |
| :--- | :--- | :--- | :--- |
| **Dispatcher / Admin** | `admin` | `citypulse2026` | Update status, append dispatcher notes, delete incidents, reload demo data |
| **Citizen (Public)** | *(No login required)* | N/A | Explore live map, report incidents, search hospitals, calculate routes |

Passwords are encrypted using PBKDF2 with SHA-256 and cryptographic salts.

---

## 6. Key Application Views

### 1. 📊 Operations Dashboard
- **Real-Time KPI Cards**: Total incidents, active high/critical emergencies, responding units, resolved cases, and verified hospitals.
- **Interactive Split View**: Prominent interactive Leaflet map side-by-side with a searchable, filterable incident log.
- **Filter Chips**: Filter instantly by category (*Accident*, *Blockage*, *Fire*, *Medical*, *Hazard*), severity (*Low*, *Medium*, *High*, *Critical*), or lifecycle status (*Reported*, *Verified*, *Responding*, *Resolved*).

### 2. 🗺️ Live Geospatial Map (Expanded)
- Fullscreen Leaflet map canvas centered on Nagpur.
- **Layer Controls**: Toggle Incidents, Hospitals, Traffic Flow, and switch between Standard OSM and Dark Matter tiles.
- **Location Geocoder**: Search any address, landmark, or street in Nagpur via Nominatim.
- **"Locate Me" Button**: Centers on browser GPS coordinates with full permission handling.
- **Active Route Drawer**: Displays computed OSRM road routes with distance (km), travel time (min), and direct Google Maps / OpenStreetMap external navigation links.

### 3. 🚨 Incident Reporting
- Report category selector with visual cards and severity priority buttons.
- **Interactive Coordinate Picker**: Click anywhere on the mini Leaflet map or click *"Use Current Location"* to place a draggable pin. Auto-fills reverse-geocoded street address.
- **Photo Upload**: Supports attaching scene photos with drag-and-drop and image thumbnail preview.
- **Immediate Propagation**: Submitting immediately broadcasts the new incident via SSE to all active browser sessions and plots its marker.

### 4. 🏥 Hospitals & Route Assistance
- Radius filter: 5 km, 10 km, 25 km, or 50 km.
- Displays verified Nagpur hospitals (AIIMS Nagpur, GMCH, Kingsway, Alexis/Max, CARE, Orange City, Platina, etc.).
- Includes verified addresses, 24x7 emergency department tags, and phone dial links (`tel:`).
- One-click **"Route to Hospital"** button calculates the genuine OSRM driving route from the user's location.

### 5. 📈 Analytics & Risk Visualization
- **Incidents by Category**: Interactive doughnut chart.
- **Severity Distribution**: Horizontal bar chart.
- **Status Lifecycle Progression**: Track cases from *Reported* $\to$ *Resolved*.
- **Daily Volume Trend**: Line chart tracking daily incident counts.
- **Nagpur Urban Risk Corridors**: Corridors summary (Sitabuldi, Wardha Road Metro, Pardi, MIDC Hingna).

### 6. ⚙️ Settings & System Diagnostics
- Administrator login / logout form.
- Live traffic API configuration monitor and setup instructions.
- Real-time SSE connection health monitor.
- Baseline demo data reset utility.

---

## 7. REST API Endpoints

### Incidents
- `GET /api/incidents`: Fetch incidents with query filters (`category`, `severity`, `status`, `search`, `limit`, `offset`).
- `POST /api/incidents`: Submit new incident (JSON or `multipart/form-data` with photo upload).
- `GET /api/incidents/<id>`: Retrieve single incident with audit trail history.
- `PATCH /api/incidents/<id>/status`: Update status and dispatcher notes (*Admin auth required*).
- `DELETE /api/incidents/<id>`: Delete incident (*Admin auth required*).
- `GET /api/incidents/stream`: Server-Sent Events (SSE) live push stream.

### Geospatial & Routing
- `GET /api/hospitals`: Query nearby hospitals (`lat`, `lon`, `radius_km`, `refresh`).
- `GET /api/route`: Calculate road driving route via OSRM (`start_lat`, `start_lon`, `end_lat`, `end_lon`).
- `GET /api/traffic/config`: Get traffic API configuration status.
- `GET /api/traffic/flow/<z>/<x>/<y>.png`: Secure backend proxy for TomTom traffic flow tiles.

### Analytics & System
- `GET /api/analytics`: Aggregate statistics from database.
- `POST /api/auth/login`: Authenticate dispatcher and receive token.
- `GET /api/auth/me`: Check active authentication state.
- `GET /api/system/status`: Health check, database metrics, and service status.
- `POST /api/system/seed`: Reset demo sample data (*Admin auth required*).
- `GET /uploads/<filename>`: Safely serve uploaded incident photos.

---

## 8. Verification & Automated Testing

CityPulse includes an automated end-to-end test suite (`test_citypulse.py`). While `run.py` is active, run:

```bash
python test_citypulse.py
```

Expected output:
```
============================================================
       RUNNING CITYPULSE FULL END-TO-END VERIFICATION
============================================================
1. Testing Frontend Static Serving...
   [PASS] GET / serves index.html
   [PASS] GET /styles.css serves valid CSS
   [PASS] GET /app.js serves valid JavaScript

2. Testing System Status API...
   [PASS] System status: healthy, City: Nagpur, Maharashtra, India, Incidents in DB: 8

3. Testing Incident Reporting, Persistence & Status Tracking...
   [PASS] Created incident #9: 'Automated Test Crash at Dharampeth Square' with status 'Reported'
   [PASS] Retrieved incident #9 with 1 audit log entries
   [PASS] Unauthorized PATCH correctly rejected (401)
   [PASS] Admin logged in successfully. Token: cp_tok_...
   [PASS] Admin updated incident #9 to 'Responding' with dispatcher notes
   [PASS] Filter by status=Responding returns 4 incidents

4. Testing Hospital Discovery & OSRM Road Routing...
   [PASS] Retrieved 10 hospitals near Nagpur (source: cache_used)
   Nearest hospital: Platina Heart Hospital & Emergency Centre (0.5 km away)
   [PASS] OSRM Road Route calculated: 3.21 km, 4.1 minutes via OSRM OpenStreetMap Driving Router
   Geometry: 126 coordinates along actual road network
   External navigation links generated: https://www.google.com/maps/dir/...

5. Testing Live Traffic Configuration Transparency...
   Traffic Provider: None (Configurable)
   Configuration Status: UNAVAILABLE_NO_API_KEY
   Integrity Boundary: Awaiting CAD/AVL Emergency Vehicle GPS Feed (Not Simulated)
   [PASS] Traffic API transparency correctly enforced.

6. Testing Real Database Analytics...
   Total incidents: 9
   Active emergencies: 5
   [PASS] Analytics reflect genuine database aggregations.
============================================================
 ALL 6 VERIFICATION TEST SUITES PASSED FLAWLESSLY! (100% SUCCESS)
============================================================
```

---

## 9. Troubleshooting & FAQ

**Q: Why does the map show OpenStreetMap tiles instead of satellite imagery?**  
A: OpenStreetMap tiles provide clear road names, street intersections, and civic addresses essential for emergency dispatch. A dark matter layer is also available in the layer toggles.

**Q: How do I enable genuine live traffic flow?**  
A: Register a free developer key at [developer.tomtom.com](https://developer.tomtom.com/), add `TOMTOM_API_KEY=your_key` to `.env`, and restart `run.py`.

**Q: What if the public OSRM or Overpass servers are experiencing intermittent downtime?**  
A: CityPulse includes automatic fallback handling:
- If OSRM is unreachable, the system generates a direct geodesic path and notifies the user with external navigation fallback links.
- If Overpass API times out, CityPulse immediately serves its verified local OSM Nagpur hospital cache, ensuring zero downtime for emergency discovery.

---

## 10. License & Attributions

- Map data and cartography: &copy; [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.
- Routing engine: [Project OSRM](http://project-osrm.org/).
- Geocoding: [Nominatim](https://nominatim.org/).
- Software: MIT License. Built for Smart City Emergency Operations.
