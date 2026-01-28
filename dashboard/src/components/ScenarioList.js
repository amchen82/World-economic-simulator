import React from 'react';
import './ScenarioList.css';

function ScenarioList({ scenarios, onRun, onViewResults, onEdit, onDelete }) {
  return (
    <div className="scenario-list">
      <h2>Scenarios</h2>
      {scenarios.length === 0 ? (
        <p className="empty-state">No scenarios yet. Create your first scenario to get started!</p>
      ) : (
        <div className="scenario-grid">
          {scenarios.map(scenario => (
            <div key={scenario.id} className="scenario-card">
              <div className="scenario-header">
                <h3>{scenario.name}</h3>
                {scenario.has_results && <span className="badge">Has Results</span>}
              </div>
              <p className="scenario-description">{scenario.description || 'No description'}</p>
              <p className="scenario-date">Created: {new Date(scenario.created_at).toLocaleString()}</p>
              
              <div className="scenario-actions">
                <button className="btn btn-primary" onClick={() => onRun(scenario.id)}>
                  Run Simulation
                </button>
                {scenario.has_results && (
                  <button className="btn btn-secondary" onClick={() => onViewResults(scenario.id)}>
                    View Results
                  </button>
                )}
                <button className="btn btn-secondary" onClick={() => onEdit(scenario.id)}>
                  Edit
                </button>
                <button className="btn btn-danger" onClick={() => {
                  if (window.confirm('Are you sure you want to delete this scenario?')) {
                    onDelete(scenario.id);
                  }
                }}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ScenarioList;
