import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './ResultsViewer.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function ResultsViewer({ scenarioId, onBack }) {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState('gdp');

  useEffect(() => {
    loadResults();
  }, [scenarioId]);

  const loadResults = async () => {
    try {
      const response = await axios.get(`/api/scenarios/${scenarioId}/results`);
      setResults(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading results:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading results...</div>;
  }

  if (!results) {
    return <div className="error">No results found for this scenario.</div>;
  }

  const metrics = {
    'GDP': 'gdp',
    'Consumption': 'consumption',
    'Investment': 'investment',
    'Government Spending': 'government_spending',
    'Unemployment Rate': 'unemployment_rate',
    'Inflation Rate': 'inflation_rate',
    'Policy Rate': 'policy_rate',
    'Average Wage': 'average_wage',
    'Employment': 'employment',
    'Budget Balance': 'budget_balance',
    'Government Debt': 'government_debt',
    'Capital Stock': 'capital_stock'
  };

  const chartData = {
    labels: results.data.time,
    datasets: [
      {
        label: Object.keys(metrics).find(key => metrics[key] === selectedMetric),
        data: results.data[selectedMetric],
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.1
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      },
      title: {
        display: true,
        text: `${Object.keys(metrics).find(key => metrics[key] === selectedMetric)} over Time`
      }
    },
    scales: {
      y: {
        beginAtZero: false
      }
    }
  };

  // Calculate summary statistics
  const data = results.data[selectedMetric];
  const mean = data.reduce((a, b) => a + b, 0) / data.length;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const final = data[data.length - 1];

  return (
    <div className="results-viewer">
      <div className="results-header">
        <button className="btn btn-secondary" onClick={onBack}>← Back</button>
        <h2>{results.scenario_name} - Results</h2>
        <p>Completed: {new Date(results.completed_at).toLocaleString()}</p>
      </div>

      <div className="metric-selector">
        <h3>Select Metric</h3>
        <div className="metric-buttons">
          {Object.entries(metrics).map(([name, key]) => (
            <button
              key={key}
              className={`metric-btn ${selectedMetric === key ? 'active' : ''}`}
              onClick={() => setSelectedMetric(key)}
            >
              {name}
            </button>
          ))}
        </div>
      </div>

      <div className="chart-container">
        <Line data={chartData} options={chartOptions} />
      </div>

      <div className="statistics">
        <h3>Summary Statistics</h3>
        <div className="stat-grid">
          <div className="stat-card">
            <span className="stat-label">Mean</span>
            <span className="stat-value">{mean.toFixed(2)}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Minimum</span>
            <span className="stat-value">{min.toFixed(2)}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Maximum</span>
            <span className="stat-value">{max.toFixed(2)}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Final Value</span>
            <span className="stat-value">{final.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsViewer;
