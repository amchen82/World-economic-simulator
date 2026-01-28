# World Economic Simulator

A comprehensive economic simulation platform where you can create scenarios, tweak parameters, run simulations, and compare outcomes through an interactive dashboard.

## Features

- 🎯 **Scenario Management**: Create and manage multiple economic scenarios
- ⚙️ **Parameter Configuration**: Adjust household, firm, government, and central bank parameters
- 🚀 **Simulation Engine**: Run economic simulations based on your custom scenarios
- 📊 **Time Series Visualization**: View economic metrics over time with interactive charts
- 🔄 **Scenario Comparison**: Compare multiple scenarios side-by-side

## Architecture

The project consists of three main components:

1. **Simulation Engine** (`simulation/`): Python-based economic model implementing:
   - Households with consumption and labor decisions
   - Firms with production and investment
   - Government with fiscal policy
   - Central bank with monetary policy (Taylor rule)

2. **REST API** (`api/`): Flask-based backend providing:
   - Scenario CRUD operations
   - Simulation execution
   - Results retrieval
   - Scenario comparison

3. **Dashboard** (`dashboard/`): React-based frontend with:
   - Scenario creation and editing
   - Parameter configuration forms
   - Interactive time-series charts (Chart.js)
   - Comparison views

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Setup

Run the setup script to install all dependencies:

```bash
./setup.sh
```

Or manually:

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install Node dependencies
cd dashboard
npm install
```

## Usage

### Starting the Application

Use the start script to launch both the API and dashboard:

```bash
./start.sh
```

Or start them manually:

```bash
# Terminal 1: Start the API server
python3 api/server.py

# Terminal 2: Start the dashboard
cd dashboard
npm start
```

The application will be available at:
- Dashboard: http://localhost:3000
- API: http://localhost:5000

### Creating and Running Scenarios

1. Click "Create New" to create a scenario
2. Enter a name and description
3. Adjust parameters as needed:
   - Time parameters (simulation duration)
   - Household parameters (consumption, labor participation)
   - Firm parameters (productivity, investment rate)
   - Government parameters (tax rate, transfers)
   - Central bank parameters (inflation target, policy rate)
4. Click "Create Scenario"
5. Click "Run Simulation" to execute
6. View results with interactive charts
7. Compare multiple scenarios to see differences

## Economic Model

The simulator implements a simplified macroeconomic model:

- **Production**: Cobb-Douglas production function
- **Labor Market**: Employment based on labor demand and supply
- **Households**: Consumption based on propensity and disposable income
- **Firms**: Investment as a fraction of profits
- **Government**: Tax collection and transfers
- **Central Bank**: Taylor rule for interest rates
- **Dynamics**: Capital accumulation, wage adjustments, inflation

## API Endpoints

- `GET /api/scenarios` - List all scenarios
- `POST /api/scenarios` - Create a new scenario
- `GET /api/scenarios/:id` - Get scenario details
- `PUT /api/scenarios/:id` - Update scenario
- `DELETE /api/scenarios/:id` - Delete scenario
- `POST /api/scenarios/:id/run` - Run simulation
- `GET /api/scenarios/:id/results` - Get simulation results
- `POST /api/compare` - Compare multiple scenarios
- `GET /api/default-parameters` - Get default parameters

## Development

### Project Structure

```
World-economic-simulator/
├── simulation/          # Python simulation engine
│   ├── __init__.py
│   └── engine.py        # Core economic model
├── api/                 # Flask REST API
│   └── server.py
├── dashboard/           # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── start.sh            # Start script
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License 
