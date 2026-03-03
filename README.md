# Chicago Traffic Camera Data Analysis

A Python command-line application for analyzing Chicago's red light and speed camera violation data. Built for CS 341 (Spring 2026) at the University of Illinois Chicago.

## Overview

This project uses a three-tier architecture (Data, Object, and Presentation layers) to query and visualize traffic camera violation data from a SQLite database containing records from the City of Chicago's traffic camera network.

## Features

| Option | Description |
|--------|-------------|
| 1 | Search for an intersection by name (supports SQL wildcards `%` and `_`) |
| 2 | List all red light and speed cameras at a given intersection |
| 3 | View the percentage breakdown of violations for a specific date |
| 4 | See the number of cameras at each intersection |
| 5 | View violation counts per intersection for a given year |
| 6 | View yearly violation totals for a specific camera ID (with plot) |
| 7 | View monthly violation totals for a camera ID and year (with plot) |
| 8 | Compare daily red light vs. speed violations for a given year (with plot) |
| 9 | Find all cameras on a given street and visualize them on a Chicago map |

## Architecture

- **DataTier.py** — Handles all SQLite queries and returns raw data
- **ObjectTier.py** — Processes data, formats output, and generates matplotlib plots
- **main.py** — Handles user input and drives the menu loop

## Setup

### Prerequisites
- Python 3.10+
- `matplotlib` library

### Installation

```bash
# Clone the repository
git clone https://github.com/KhangN65719/Chicago-Traffic-Camera-Data-Analysis.git
cd Chicago-Traffic-Camera-Data-Analysis

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install matplotlib
```

### Database

The SQLite database is not included in this repository due to file size. To obtain it, download the Chicago traffic camera violation datasets from the [Chicago Data Portal](https://data.cityofchicago.org/) and place the `.db` file at `Data/chicago-traffic-cameras.db`.

### Running

```bash
python3 main.py
```

## Technologies

- Python 3
- SQLite3
- Matplotlib
