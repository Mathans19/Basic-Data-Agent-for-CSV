
# Basic CSV Data Agent

A simple Natural Language interface for querying and analyzing CSV data files without writing any code.

## Overview

This project implements a Python-based agent that can answer questions about CSV data using natural language queries. The agent loads CSV files and allows users to extract insights, statistics, and filter data using simple English questions.

## Features

- Load and analyze any CSV file
- Ask questions in natural language about your data
- Get statistical summaries, distributions, and insights
- Filter data based on column values
- Find correlations between numerical columns

## Repository Structure

```
├── README.md
├── data/
│   ├── hr.csv
│   ├── dress.csv 
│   └── myntra.csv
├── agent/
│   └── basic_data_agent.py
└── test_agent.py
```

## Getting Started

### Prerequisites

- Python 3.6+
- pandas
- numpy

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/basic-csv-data-agent.git
   cd basic-csv-data-agent
   ```

2. Install dependencies:
   ```
   pip install pandas numpy
   ```

### Usage

Run the interactive test script and provide the path to your CSV file:

```
python test_agent.py data/your_file.csv
```

Then simply type your questions about the data when prompted.

## Sample Questions by Dataset

### HR Dataset (`hr.csv`)

- "How many rows are in this dataset?"
- "Show me all columns"
- "What's the average monthly income?"
- "Show me the distribution of Department"
- "What's the relationship between age and monthly income?"
- "How many employees have attrition = Yes?"
- "What is the gender distribution?"
- "Show me employees where MonthlyIncome is > 5000"

### Dress Dataset (`dress.csv`)

- "How many rows are in this dataset?"
- "What columns are in this dataset?"
- "Show me the distribution of Style"
- "What are the top 5 highest rated dresses?"
- "How many dresses are recommended?"
- "Show me the distribution of Season"
- "What are the most common materials used?"
- "What's the average rating?"

### Myntra Dataset (`myntra.csv`)

- "How many products are in the dataset?"
- "What's the average price?"
- "Show me the distribution of ProductBrand"
- "What's the gender distribution?"
- "Show me products where price is > 1000"
- "What are the most common primary colors?"
- "How many unique brands are there?"
- "What are the top 5 most expensive products?"

## Extending the Agent

To add more query capabilities, modify the `process_query` method in the `CustomCSVDataAgent` class to handle additional patterns and questions.