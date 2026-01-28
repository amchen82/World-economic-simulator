"""REST API for World Economic Simulator"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from typing import Dict, Any
from simulation.engine import EconomicSimulator, SimulationParameters

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# In-memory storage for scenarios and results
# Note: Data is not persisted and will be lost on server restart
scenarios: Dict[str, Dict[str, Any]] = {}
results: Dict[str, Dict[str, Any]] = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'World Economic Simulator API'})


@app.route('/api/scenarios', methods=['GET'])
def list_scenarios():
    """List all scenarios"""
    scenario_list = [
        {
            'id': scenario_id,
            'name': scenario['name'],
            'description': scenario['description'],
            'created_at': scenario['created_at'],
            'has_results': scenario_id in results
        }
        for scenario_id, scenario in scenarios.items()
    ]
    return jsonify(scenario_list)


@app.route('/api/scenarios', methods=['POST'])
def create_scenario():
    """Create a new scenario"""
    data = request.json
    
    # Validate parameters if provided
    parameters = data.get('parameters', {})
    validation_errors = []
    
    if 'time_steps' in parameters and (parameters['time_steps'] < 1 or parameters['time_steps'] > 10000):
        validation_errors.append('time_steps must be between 1 and 10000')
    if 'num_households' in parameters and parameters['num_households'] < 1:
        validation_errors.append('num_households must be positive')
    if 'num_firms' in parameters and parameters['num_firms'] < 1:
        validation_errors.append('num_firms must be positive')
    if 'tax_rate' in parameters and (parameters['tax_rate'] < 0 or parameters['tax_rate'] > 1):
        validation_errors.append('tax_rate must be between 0 and 1')
    if 'consumption_propensity' in parameters and (parameters['consumption_propensity'] < 0 or parameters['consumption_propensity'] > 1):
        validation_errors.append('consumption_propensity must be between 0 and 1')
    if 'labor_participation_rate' in parameters and (parameters['labor_participation_rate'] < 0 or parameters['labor_participation_rate'] > 1):
        validation_errors.append('labor_participation_rate must be between 0 and 1')
    
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
    
    scenario_id = str(uuid.uuid4())
    scenario = {
        'id': scenario_id,
        'name': data.get('name', 'Unnamed Scenario'),
        'description': data.get('description', ''),
        'created_at': datetime.utcnow().isoformat(),
        'parameters': parameters
    }
    
    scenarios[scenario_id] = scenario
    return jsonify(scenario), 201


@app.route('/api/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Get a specific scenario"""
    if scenario_id not in scenarios:
        return jsonify({'error': 'Scenario not found'}), 404
    
    return jsonify(scenarios[scenario_id])


@app.route('/api/scenarios/<scenario_id>', methods=['PUT'])
def update_scenario(scenario_id):
    """Update a scenario"""
    if scenario_id not in scenarios:
        return jsonify({'error': 'Scenario not found'}), 404
    
    data = request.json
    scenario = scenarios[scenario_id]
    
    if 'name' in data:
        scenario['name'] = data['name']
    if 'description' in data:
        scenario['description'] = data['description']
    if 'parameters' in data:
        scenario['parameters'] = data['parameters']
    
    scenarios[scenario_id] = scenario
    return jsonify(scenario)


@app.route('/api/scenarios/<scenario_id>', methods=['DELETE'])
def delete_scenario(scenario_id):
    """Delete a scenario"""
    if scenario_id not in scenarios:
        return jsonify({'error': 'Scenario not found'}), 404
    
    del scenarios[scenario_id]
    if scenario_id in results:
        del results[scenario_id]
    
    return '', 204


@app.route('/api/scenarios/<scenario_id>/run', methods=['POST'])
def run_simulation(scenario_id):
    """Run simulation for a scenario"""
    if scenario_id not in scenarios:
        return jsonify({'error': 'Scenario not found'}), 404
    
    scenario = scenarios[scenario_id]
    params_dict = scenario.get('parameters', {})
    
    try:
        # Create simulation parameters
        params = SimulationParameters(**params_dict)
        
        # Run simulation
        simulator = EconomicSimulator(params)
        simulator.run()
        
        # Store results
        simulation_results = simulator.get_results()
        results[scenario_id] = {
            'scenario_id': scenario_id,
            'scenario_name': scenario['name'],
            'completed_at': datetime.utcnow().isoformat(),
            'data': simulation_results
        }
        
        return jsonify({
            'message': 'Simulation completed',
            'scenario_id': scenario_id
        })
    except Exception as e:
        return jsonify({
            'error': 'Simulation failed',
            'details': str(e)
        }), 500


@app.route('/api/scenarios/<scenario_id>/results', methods=['GET'])
def get_results(scenario_id):
    """Get simulation results for a scenario"""
    if scenario_id not in results:
        return jsonify({'error': 'No results found for this scenario'}), 404
    
    return jsonify(results[scenario_id])


@app.route('/api/compare', methods=['POST'])
def compare_scenarios():
    """Compare multiple scenarios"""
    data = request.json
    scenario_ids = data.get('scenario_ids', [])
    
    if not scenario_ids:
        return jsonify({'error': 'No scenario IDs provided'}), 400
    
    # Validate all scenarios exist and have results
    missing_scenarios = []
    missing_results = []
    
    for scenario_id in scenario_ids:
        if scenario_id not in scenarios:
            missing_scenarios.append(scenario_id)
        elif scenario_id not in results:
            missing_results.append(scenario_id)
    
    if missing_scenarios:
        return jsonify({
            'error': 'Some scenarios not found',
            'missing_scenarios': missing_scenarios
        }), 404
    
    if missing_results:
        return jsonify({
            'error': 'Some scenarios do not have results. Please run simulations first.',
            'scenarios_without_results': [scenarios[sid]['name'] for sid in missing_results]
        }), 400
    
    comparison = []
    for scenario_id in scenario_ids:
        comparison.append({
            'scenario_id': scenario_id,
            'scenario_name': scenarios[scenario_id]['name'],
            'parameters': scenarios[scenario_id]['parameters'],
            'results': results[scenario_id]['data']
        })
    
    return jsonify({'scenarios': comparison})


@app.route('/api/default-parameters', methods=['GET'])
def get_default_parameters():
    """Get default simulation parameters"""
    params = SimulationParameters()
    return jsonify({
        'time_steps': params.time_steps,
        'num_households': params.num_households,
        'consumption_propensity': params.consumption_propensity,
        'labor_participation_rate': params.labor_participation_rate,
        'num_firms': params.num_firms,
        'productivity': params.productivity,
        'wage_baseline': params.wage_baseline,
        'investment_rate': params.investment_rate,
        'tax_rate': params.tax_rate,
        'transfer_per_capita': params.transfer_per_capita,
        'inflation_target': params.inflation_target,
        'policy_rate_baseline': params.policy_rate_baseline,
        'taylor_rule_sensitivity': params.taylor_rule_sensitivity,
        'initial_capital': params.initial_capital,
        'initial_price_level': params.initial_price_level,
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
