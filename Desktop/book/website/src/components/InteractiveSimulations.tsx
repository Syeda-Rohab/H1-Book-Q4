/**
 * Interactive Simulations Component
 *
 * Features:
 * - Robot Arm Kinematics simulation
 * - Sensor Range visualization
 * - Path Planning demonstration
 * - Balance Control simulation
 * - Interactive controls
 */

import React, { useState, useRef, useEffect } from 'react';
import styles from './InteractiveSimulations.module.css';

type SimulationType = 'robot-arm' | 'sensors' | 'path-planning' | 'balance';

interface Simulation {
  id: SimulationType;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  icon: string;
}

const SIMULATIONS: Simulation[] = [
  {
    id: 'robot-arm',
    name: 'Robot Arm Kinematics',
    description: 'Control a 2-link robot arm and see inverse kinematics in action',
    difficulty: 'intermediate',
    icon: '🦾',
  },
  {
    id: 'sensors',
    name: 'Sensor Range Visualization',
    description: 'Explore how different sensors detect objects in their environment',
    difficulty: 'beginner',
    icon: '📡',
  },
  {
    id: 'path-planning',
    name: 'Path Planning',
    description: 'Watch A* algorithm find optimal paths around obstacles',
    difficulty: 'advanced',
    icon: '🗺️',
  },
  {
    id: 'balance',
    name: 'Balance Control',
    description: 'Adjust PID parameters to balance an inverted pendulum',
    difficulty: 'advanced',
    icon: '⚖️',
  },
];

// Robot Arm Simulation Component
function RobotArmSimulation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [angle1, setAngle1] = useState(45);
  const [angle2, setAngle2] = useState(-30);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Setup
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const link1Length = 80;
    const link2Length = 60;

    // Convert angles to radians
    const a1 = (angle1 * Math.PI) / 180;
    const a2 = (angle2 * Math.PI) / 180;

    // Calculate positions
    const joint1X = centerX + link1Length * Math.cos(a1);
    const joint1Y = centerY + link1Length * Math.sin(a1);
    const endX = joint1X + link2Length * Math.cos(a1 + a2);
    const endY = joint1Y + link2Length * Math.sin(a1 + a2);

    // Draw base
    ctx.beginPath();
    ctx.arc(centerX, centerY, 8, 0, 2 * Math.PI);
    ctx.fillStyle = '#333';
    ctx.fill();

    // Draw link 1
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(joint1X, joint1Y);
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Draw joint 1
    ctx.beginPath();
    ctx.arc(joint1X, joint1Y, 6, 0, 2 * Math.PI);
    ctx.fillStyle = '#f5576c';
    ctx.fill();

    // Draw link 2
    ctx.beginPath();
    ctx.moveTo(joint1X, joint1Y);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = '#764ba2';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Draw end effector
    ctx.beginPath();
    ctx.arc(endX, endY, 8, 0, 2 * Math.PI);
    ctx.fillStyle = '#38ef7d';
    ctx.fill();

    // Draw position text
    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.fillText(`End Position: (${Math.round(endX - centerX)}, ${Math.round(endY - centerY)})`, 10, 20);
  }, [angle1, angle2]);

  return (
    <div className={styles.simulationContent}>
      <canvas ref={canvasRef} width={400} height={300} className={styles.canvas} />
      <div className={styles.controls}>
        <div className={styles.control}>
          <label>Joint 1 Angle: {angle1}°</label>
          <input
            type="range"
            min="-180"
            max="180"
            value={angle1}
            onChange={(e) => setAngle1(Number(e.target.value))}
          />
        </div>
        <div className={styles.control}>
          <label>Joint 2 Angle: {angle2}°</label>
          <input
            type="range"
            min="-180"
            max="180"
            value={angle2}
            onChange={(e) => setAngle2(Number(e.target.value))}
          />
        </div>
      </div>
    </div>
  );
}

// Sensor Simulation Component
function SensorSimulation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [sensorAngle, setSensorAngle] = useState(0);
  const [sensorRange, setSensorRange] = useState(100);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height - 50;

    // Draw robot
    ctx.beginPath();
    ctx.arc(centerX, centerY, 20, 0, 2 * Math.PI);
    ctx.fillStyle = '#667eea';
    ctx.fill();

    // Draw sensor cone
    const angleRad = (sensorAngle * Math.PI) / 180;
    const coneAngle = Math.PI / 6;

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, sensorRange, angleRad - coneAngle, angleRad + coneAngle);
    ctx.closePath();
    ctx.fillStyle = 'rgba(102, 126, 234, 0.2)';
    ctx.fill();
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw obstacles
    const obstacles = [
      { x: 200, y: 150, radius: 15 },
      { x: 300, y: 100, radius: 20 },
      { x: 100, y: 120, radius: 18 },
    ];

    obstacles.forEach(obs => {
      ctx.beginPath();
      ctx.arc(obs.x, obs.y, obs.radius, 0, 2 * Math.PI);

      // Check if obstacle is in sensor range
      const dx = obs.x - centerX;
      const dy = obs.y - centerY;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const obsAngle = Math.atan2(dy, dx);

      const inRange = distance < sensorRange &&
                     Math.abs(obsAngle - angleRad) < coneAngle;

      ctx.fillStyle = inRange ? '#f5576c' : '#ccc';
      ctx.fill();
    });
  }, [sensorAngle, sensorRange]);

  return (
    <div className={styles.simulationContent}>
      <canvas ref={canvasRef} width={400} height={300} className={styles.canvas} />
      <div className={styles.controls}>
        <div className={styles.control}>
          <label>Sensor Angle: {sensorAngle}°</label>
          <input
            type="range"
            min="-90"
            max="90"
            value={sensorAngle}
            onChange={(e) => setSensorAngle(Number(e.target.value))}
          />
        </div>
        <div className={styles.control}>
          <label>Sensor Range: {sensorRange}px</label>
          <input
            type="range"
            min="50"
            max="150"
            value={sensorRange}
            onChange={(e) => setSensorRange(Number(e.target.value))}
          />
        </div>
      </div>
    </div>
  );
}

// Main Component
export default function InteractiveSimulations(): JSX.Element {
  const [selectedSim, setSelectedSim] = useState<SimulationType | null>(null);

  const renderSimulation = () => {
    switch (selectedSim) {
      case 'robot-arm':
        return <RobotArmSimulation />;
      case 'sensors':
        return <SensorSimulation />;
      case 'path-planning':
        return (
          <div className={styles.comingSoon}>
            <p>🚧 Path Planning simulation coming soon!</p>
            <p>This will demonstrate A* algorithm for optimal path finding.</p>
          </div>
        );
      case 'balance':
        return (
          <div className={styles.comingSoon}>
            <p>🚧 Balance Control simulation coming soon!</p>
            <p>This will let you tune PID parameters for an inverted pendulum.</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Interactive Simulations</h2>
        <p>Learn by doing - interact with robotics simulations</p>
      </div>

      {!selectedSim ? (
        <div className={styles.grid}>
          {SIMULATIONS.map((sim) => (
            <div
              key={sim.id}
              className={styles.card}
              onClick={() => setSelectedSim(sim.id)}
            >
              <div className={styles.cardIcon}>{sim.icon}</div>
              <h3>{sim.name}</h3>
              <p>{sim.description}</p>
              <span className={`${styles.difficulty} ${styles[sim.difficulty]}`}>
                {sim.difficulty}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className={styles.simulationView}>
          <div className={styles.simHeader}>
            <button
              className={styles.backButton}
              onClick={() => setSelectedSim(null)}
            >
              ← Back to Simulations
            </button>
            <h3>{SIMULATIONS.find(s => s.id === selectedSim)?.name}</h3>
          </div>
          {renderSimulation()}
          <div className={styles.simInfo}>
            <p>{SIMULATIONS.find(s => s.id === selectedSim)?.description}</p>
          </div>
        </div>
      )}
    </div>
  );
}
