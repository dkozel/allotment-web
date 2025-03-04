import { useEffect, useState } from "react";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

function fetchDevices() {
  return axios.get(`${API_URL}/devices`).then((res) => res.data);
}

function fetchMeasurements() {
  return axios.get(`${API_URL}/measurements`).then((res) => res.data);
}

function App() {
  const { data: devices, error: devicesError, isLoading: devicesLoading } = useQuery({ queryKey: ["devices"], queryFn: fetchDevices });

  const { data: measurements, error: measurementsError, isLoading: measurementsLoading } = useQuery({ queryKey: ["measurements"], queryFn: fetchMeasurements });

  const chartData = {
    labels: measurements?.map((m) => new Date(m.time).toLocaleTimeString()),
    datasets: [
      {
        label: "Temperature (°C)",
        data: measurements?.map((m) => m.tempC ?? null),
        borderColor: "#f87171",
        backgroundColor: "rgba(248, 113, 113, 0.2)",
      },
      {
        label: "Humidity (%)",
        data: measurements?.map((m) => m.humidity ?? null),
        borderColor: "#60a5fa",
        backgroundColor: "rgba(96, 165, 250, 0.2)",
      },
    ],
  };

  return (
    <div className="container">
      <h1>Device & Measurement Data</h1>

      {/* Chart Section */}
      <div className="card">
        <h2>Temperature & Humidity Trends</h2>
        {measurements && measurements.length > 0 ? <Line data={chartData} /> : <p>No measurement data available.</p>}
      </div>

      {/* Devices Section */}
      <div className="card">
        <h2>Devices</h2>
        {devicesLoading ? (
          <p>Loading devices...</p>
        ) : devicesError ? (
          <p className="error">Error: {devicesError.message}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Device ID</th>
                <th>DevEUI</th>
              </tr>
            </thead>
            <tbody>
              {devices?.map((device) => (
                <tr key={device.id}>
                  <td>{device.id}</td>
                  <td>{device.deviceID}</td>
                  <td>{device.devEui || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Measurements Section */}
      <div className="card">
        <h2>Measurements</h2>
        {measurementsLoading ? (
          <p>Loading measurements...</p>
        ) : measurementsError ? (
          <p className="error">Error: {measurementsError.message}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Device ID</th>
                <th>Time</th>
                <th>Temp (°C)</th>
                <th>Humidity (%)</th>
                <th>Battery (V)</th>
              </tr>
            </thead>
            <tbody>
              {measurements?.map((m) => (
                <tr key={m.id}>
                  <td>{m.id}</td>
                  <td>{m.deviceId}</td>
                  <td>{new Date(m.time).toLocaleString()}</td>
                  <td>{m.tempC ?? "N/A"}</td>
                  <td>{m.humidity ?? "N/A"}</td>
                  <td>{m.batteryV ?? "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;
