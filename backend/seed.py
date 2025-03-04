import random
from datetime import datetime, timedelta
from prisma import Prisma

# Initialize Prisma Client
db = Prisma()

# Sample Device IDs
DEVICE_1_ID = "device_123"
DEVICE_2_ID = "device_456"

# ✅ Connect to the database
db.connect()

# ✅ 1. Clear Existing Data
print("⚠️ Clearing existing data...")
db.measurement.delete_many()  # Clear all measurements first (to avoid FK errors)
db.device.delete_many()       # Clear all devices
print("✅ Existing data cleared!")

# ✅ 2. Insert Two Devices
devices = [
    {"deviceID": DEVICE_1_ID, "devEui": "AA-BB-CC-01"},
    {"deviceID": DEVICE_2_ID, "devEui": "AA-BB-CC-02"},
]

for device in devices:
    db.device.create(data=device)

print("✅ Devices inserted!")

# ✅ 3. Insert 200+ Measurement Records (15-min intervals)
start_time = datetime.now() - timedelta(days=2)  # Start 2 days ago
num_entries = 200  # Total unique timestamps
measurements = []

for i in range(num_entries):
    # Base timestamp for this interval
    base_time = start_time + timedelta(minutes=15 * i)
    
    # For the first device, use the base time; for the second, add 1 second.
    adjusted_times = [base_time, base_time + timedelta(seconds=1)]
    
    for device_id, adjusted_time in zip([DEVICE_1_ID, DEVICE_2_ID], adjusted_times):
        measurements.append({
            "deviceId": device_id,
            "time": adjusted_time,
            "tempC": round(random.uniform(15, 30), 2),
            "tempCExt": round(random.uniform(5, 20), 2),
            "humidity": round(random.uniform(30, 90), 2),
            "batteryV": round(random.uniform(3.0, 4.2), 2),
            "rssidB": round(random.uniform(-80, -30), 2),
            "snrdB": round(random.uniform(5, 30), 2),
        })

# ✅ Bulk Insert Measurements
db.measurement.create_many(data=measurements)
print(f"✅ Inserted {len(measurements)} measurement records!")

# ✅ Disconnect from DB
db.disconnect()
print("✅ Seed script completed successfully!")
