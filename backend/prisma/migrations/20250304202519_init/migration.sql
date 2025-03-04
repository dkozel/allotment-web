-- CreateTable
CREATE TABLE "Device" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "deviceID" TEXT NOT NULL,
    "devEui" TEXT
);

-- CreateTable
CREATE TABLE "Measurement" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "deviceId" TEXT NOT NULL,
    "time" DATETIME NOT NULL,
    "tempC" REAL,
    "tempCExt" REAL,
    "humidity" REAL,
    "batteryV" REAL,
    "rssidB" REAL,
    "snrdB" REAL,
    CONSTRAINT "Measurement_deviceId_fkey" FOREIGN KEY ("deviceId") REFERENCES "Device" ("deviceID") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Device_deviceID_key" ON "Device"("deviceID");

-- CreateIndex
CREATE UNIQUE INDEX "Measurement_time_key" ON "Measurement"("time");
