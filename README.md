# ECU Log Data Analyzer

A Python-based web application for visualizing and analyzing ECU (Engine Control Unit) log data from CSV files. Built with Dash and Plotly for interactive data exploration.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.0+-green.svg)

## Features

- 📊 **Interactive Plotting** - Visualize multiple ECU parameters on dual y-axes
- 📁 **Drag & Drop Upload** - Easy CSV file loading with drag-and-drop interface
- 🎯 **Field Selection** - Choose specific parameters to plot from your data
- ⏱️ **Time Range Filtering** - Focus on specific time windows in your logs
- 📈 **Statistical Summary** - View key statistics (mean, std, min, max) for selected fields
- 🎨 **Dual Y-Axis Support** - Plot parameters with different scales simultaneously
- 🖥️ **Auto-Launch** - Automatically opens in your default browser

## Screenshots

### Main Interface
Upload your ECU log files and select parameters to visualize.

### Interactive Plots
Zoom, pan, and hover over data points to explore your ECU logs in detail.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ecu-log-analyzer.git
cd ecu-log-analyzer
```

2. Install required dependencies:
```bash
pip install dash plotly pandas
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python ecu_log_analyzer.py
```

2. The application will automatically open in your default web browser at `http://127.0.0.1:8050/`

3. Upload your ECU log CSV file:
   - Drag and drop your CSV file into the upload area, or
   - Click "Select Files" to browse for your file

4. Select fields to plot:
   - Choose parameters for the left Y-axis
   - Optionally add parameters for the right Y-axis (for different scales)
   - Select your X-axis field (defaults to "Time" if available)

5. Adjust the time range slider to focus on specific portions of your data

6. Click "Update Plot" to visualize your data

7. Click "Clear Plot" to reset the visualization

## CSV File Format

Your CSV file should have:
- A header row with column names
- Numerical data for plotting
- Optionally, a "Time" column for the X-axis

Example CSV structure:
```csv
Time,RPM,Speed,Throttle,Temperature
0.0,1000,0,0,85
0.1,1200,5,15,86
0.2,1500,10,25,87
...
```

## Features in Detail

### Dual Y-Axis Support
Plot parameters with different scales on separate axes for better visualization:
- **Left Y-Axis**: Primary parameters (solid lines)
- **Right Y-Axis**: Secondary parameters (dashed lines)

### Time Range Filtering
Use the interactive slider to:
- Focus on specific time windows
- Exclude irrelevant data from analysis
- Update statistics for the selected range

### Statistical Summary
View real-time statistics for selected fields:
- Count of data points
- Mean value
- Standard deviation
- Minimum and maximum values

## Dependencies

- **dash** - Web application framework
- **plotly** - Interactive plotting library
- **pandas** - Data manipulation and analysis
- **Python 3.7+** - Core runtime

## Project Structure

```
ecu-log-analyzer/
│
├── ecu_log_analyzer.py    # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── sample_data/           # Sample ECU log files (optional)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Application doesn't open automatically
- Manually navigate to `http://127.0.0.1:8050/` in your browser
- Check if port 8050 is already in use

### CSV file won't upload
- Ensure the file has a `.csv` extension
- Check that the CSV is properly formatted with headers
- Verify the file isn't corrupted

### Plot doesn't update
- Make sure you've selected at least one field for the left Y-axis
- Click the "Update Plot" button after making selections
- Check the browser console for any error messages

## Acknowledgments

- Built with [Dash](https://dash.plotly.com/) by Plotly
- Visualizations powered by [Plotly](https://plotly.com/)
- Data handling by [Pandas](https://pandas.pydata.org/)


---

⭐ If you find this tool useful, please consider giving it a star!
