import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ScenarioEditor.css';

function ScenarioEditor({ scenarioId, onSave, onCancel }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [parameters, setParameters] = useState({});
  const [defaultParams, setDefaultParams] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [scenarioId]);

  const loadData = async () => {
    try {
      // Load default parameters
      const defaultResponse = await axios.get('/api/default-parameters');
      setDefaultParams(defaultResponse.data);
      
      if (scenarioId) {
        // Load existing scenario
        const scenarioResponse = await axios.get(`/api/scenarios/${scenarioId}`);
        setName(scenarioResponse.data.name);
        setDescription(scenarioResponse.data.description);
        setParameters(scenarioResponse.data.parameters || {});
      } else {
        // Use defaults for new scenario
        setParameters(defaultResponse.data);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const handleParameterChange = (key, value) => {
    setParameters({
      ...parameters,
      [key]: parseFloat(value) || 0
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      name,
      description,
      parameters
    });
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  const parameterGroups = {
    'Time Parameters': ['time_steps'],
    'Household Parameters': ['num_households', 'consumption_propensity', 'labor_participation_rate'],
    'Firm Parameters': ['num_firms', 'productivity', 'wage_baseline', 'investment_rate'],
    'Government Parameters': ['tax_rate', 'transfer_per_capita'],
    'Central Bank Parameters': ['inflation_target', 'policy_rate_baseline', 'taylor_rule_sensitivity'],
    'Initial Conditions': ['initial_capital', 'initial_price_level']
  };

  return (
    <div className="scenario-editor">
      <h2>{scenarioId ? 'Edit Scenario' : 'Create New Scenario'}</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Basic Information</h3>
          <div className="form-group">
            <label>Scenario Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="e.g., High Tax Scenario"
            />
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what this scenario tests..."
              rows="3"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>Simulation Parameters</h3>
          {Object.entries(parameterGroups).map(([groupName, paramKeys]) => (
            <div key={groupName} className="param-group">
              <h4>{groupName}</h4>
              <div className="param-grid">
                {paramKeys.map(key => (
                  <div key={key} className="form-group">
                    <label>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</label>
                    <input
                      type="number"
                      step="any"
                      value={parameters[key] !== undefined ? parameters[key] : defaultParams[key]}
                      onChange={(e) => handleParameterChange(key, e.target.value)}
                    />
                    <small>Default: {defaultParams[key]}</small>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {scenarioId ? 'Update Scenario' : 'Create Scenario'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default ScenarioEditor;
