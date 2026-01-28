import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import './ComparisonView.css';

function ComparisonView({ scenarios, onBack }) {
  const [selectedScenarios, setSelectedScenarios] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('gdp');
  const [loading, setLoading] = useState(false);

  const handleScenarioToggle = (scenarioId) => {
    if (selectedScenarios.includes(scenarioId)) {
      setSelectedScenarios(selectedScenarios.filter(id => id !== scenarioId));
    } else {
      setSelectedScenarios([...selectedScenarios, scenarioId]);
    }
  };

  const loadComparison = async () => {
    if (selectedScenarios.length < 2) {
      alert('Please select at least 2 scenarios to compare');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/compare', {
        scenario_ids: selectedScenarios
      });
      setComparisonData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading comparison:', error);
      setLoading(false);
    }
  };

  const metrics = {
    'GDP': 'gdp',
    'Consumption': 'consumption',
    'Investment': 'investment',
    'Government Spending': 'government_spending',
    'Unemployment Rate': 'unemployment_rate',
    'Inflation Rate': 'inflation_rate',
    'Policy Rate': 'policy_rate',
    'Average Wage': 'average_wage'
  };

  const colors = [
    '#667eea',
    '#f59e0b',
    '#10b981',
    '#ef4444',
    '#8b5cf6',
    '#ec4899'
  ];

  let chartData = null;
  if (comparisonData) {
    chartData = {
      labels: comparisonData.scenarios[0].results.time,
      datasets: comparisonData.scenarios.map((scenario, index) => ({
        label: scenario.scenario_name,
        data: scenario.results[selectedMetric],
        borderColor: colors[index % colors.length],
        backgroundColor: `${colors[index % colors.length]}20`,
        tension: 0.1
      }))
    };
  }

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
        text: `Comparison: ${Object.keys(metrics).find(key => metrics[key] === selectedMetric)}`
      }
    },
    scales: {
      y: {
        beginAtZero: false
      }
    }
  };

  return (
    <div className="comparison-view">
      <div className="comparison-header">
        <button className="btn btn-secondary" onClick={onBack}>← Back</button>
        <h2>Compare Scenarios</h2>
      </div>

      <div className="scenario-selection">
        <h3>Select Scenarios to Compare</h3>
        <div className="scenario-checkboxes">
          {scenarios.map(scenario => (
            <label key={scenario.id} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedScenarios.includes(scenario.id)}
                onChange={() => handleScenarioToggle(scenario.id)}
              />
              <span>{scenario.name}</span>
            </label>
          ))}
        </div>
        <button
          className="btn btn-primary"
          onClick={loadComparison}
          disabled={selectedScenarios.length < 2}
        >
          Compare Selected Scenarios
        </button>
      </div>

      {loading && <div className="loading">Loading comparison...</div>}

      {comparisonData && !loading && (
        <>
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

          <div className="comparison-table">
            <h3>Final Values Comparison</h3>
            <table>
              <thead>
                <tr>
                  <th>Scenario</th>
                  {Object.keys(metrics).map(name => (
                    <th key={name}>{name}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {comparisonData.scenarios.map((scenario, index) => (
                  <tr key={scenario.scenario_id}>
                    <td style={{ color: colors[index % colors.length], fontWeight: 'bold' }}>
                      {scenario.scenario_name}
                    </td>
                    {Object.values(metrics).map(metric => {
                      const values = scenario.results[metric];
                      const finalValue = values[values.length - 1];
                      return <td key={metric}>{finalValue.toFixed(2)}</td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

export default ComparisonView;
