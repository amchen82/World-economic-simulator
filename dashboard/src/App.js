import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ScenarioList from './components/ScenarioList';
import ScenarioEditor from './components/ScenarioEditor';
import ResultsViewer from './components/ResultsViewer';
import ComparisonView from './components/ComparisonView';
import './App.css';

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [view, setView] = useState('list'); // 'list', 'create', 'edit', 'results', 'compare'
  const [compareScenarios, setCompareScenarios] = useState([]);

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      const response = await axios.get('/api/scenarios');
      setScenarios(response.data);
    } catch (error) {
      console.error('Error loading scenarios:', error);
    }
  };

  const handleCreateScenario = async (scenarioData) => {
    try {
      await axios.post('/api/scenarios', scenarioData);
      await loadScenarios();
      setView('list');
    } catch (error) {
      console.error('Error creating scenario:', error);
    }
  };

  const handleUpdateScenario = async (scenarioId, scenarioData) => {
    try {
      await axios.put(`/api/scenarios/${scenarioId}`, scenarioData);
      await loadScenarios();
      setView('list');
    } catch (error) {
      console.error('Error updating scenario:', error);
    }
  };

  const handleDeleteScenario = async (scenarioId) => {
    try {
      await axios.delete(`/api/scenarios/${scenarioId}`);
      await loadScenarios();
    } catch (error) {
      console.error('Error deleting scenario:', error);
    }
  };

  const handleRunSimulation = async (scenarioId) => {
    try {
      await axios.post(`/api/scenarios/${scenarioId}/run`);
      await loadScenarios();
      setSelectedScenario(scenarioId);
      setView('results');
    } catch (error) {
      console.error('Error running simulation:', error);
    }
  };

  const handleViewResults = (scenarioId) => {
    setSelectedScenario(scenarioId);
    setView('results');
  };

  const handleEditScenario = (scenarioId) => {
    setSelectedScenario(scenarioId);
    setView('edit');
  };

  const handleCompare = (scenarioIds) => {
    setCompareScenarios(scenarioIds);
    setView('compare');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌍 World Economic Simulator</h1>
        <p>Create scenarios, tweak parameters, and compare simulation outcomes</p>
      </header>

      <nav className="App-nav">
        <button onClick={() => setView('list')} className={view === 'list' ? 'active' : ''}>
          Scenarios
        </button>
        <button onClick={() => setView('create')} className={view === 'create' ? 'active' : ''}>
          Create New
        </button>
        {scenarios.filter(s => s.has_results).length > 1 && (
          <button onClick={() => setView('compare')} className={view === 'compare' ? 'active' : ''}>
            Compare
          </button>
        )}
      </nav>

      <main className="App-main">
        {view === 'list' && (
          <ScenarioList
            scenarios={scenarios}
            onRun={handleRunSimulation}
            onViewResults={handleViewResults}
            onEdit={handleEditScenario}
            onDelete={handleDeleteScenario}
          />
        )}

        {view === 'create' && (
          <ScenarioEditor
            onSave={handleCreateScenario}
            onCancel={() => setView('list')}
          />
        )}

        {view === 'edit' && selectedScenario && (
          <ScenarioEditor
            scenarioId={selectedScenario}
            onSave={(data) => handleUpdateScenario(selectedScenario, data)}
            onCancel={() => setView('list')}
          />
        )}

        {view === 'results' && selectedScenario && (
          <ResultsViewer
            scenarioId={selectedScenario}
            onBack={() => setView('list')}
          />
        )}

        {view === 'compare' && (
          <ComparisonView
            scenarios={scenarios.filter(s => s.has_results)}
            onBack={() => setView('list')}
          />
        )}
      </main>
    </div>
  );
}

export default App;
