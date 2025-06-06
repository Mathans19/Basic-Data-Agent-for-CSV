# CSV Data Analyst with Groq AI

A Streamlit web application that allows users to upload CSV files and ask natural language questions about their data using Groq's AI models.

## Features

- **CSV File Upload**: Easy drag-and-drop CSV file uploading
- **Data Preview**: Automatically displays the first few rows of uploaded data
- **Natural Language Queries**: Ask questions about your data in plain English
- **AI-Powered Analysis**: Uses Groq's LLaMA 3 70B model for intelligent data analysis
- **Interactive Interface**: Clean, user-friendly Streamlit interface

## Prerequisites

- Python 3.7 or higher
- Groq API key (sign up at [Groq Console](https://console.groq.com/))

## Installation

1. **Clone or download the repository**
   ```bash
   git clone <your-repo-url>
   cd csv-data-analyst
   ```

2. **Install required dependencies**
   ```bash
   pip install streamlit pandas langchain-groq python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   Replace `your_groq_api_key_here` with your actual Groq API key.

## Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Upload your CSV file**
   - Click on "Browse files" or drag and drop your CSV file
   - The app will automatically load and display a preview of your data

3. **Ask questions about your data**
   - Type your question in the text input field
   - Examples of questions you can ask:
     - "What is the average value in the price column?"
     - "How many rows contain missing values?"
     - "What are the top 5 categories by count?"
     - "Show me summary statistics for all numerical columns"
     - "What trends do you see in the data?"

4. **View AI-generated insights**
   - The AI will analyze your entire dataset and provide detailed answers
   - Results are displayed in an easy-to-read format

## Supported File Types

- CSV files (.csv)
- Files should be properly formatted with headers in the first row

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for accessing the AI model | Yes |

## Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `langchain-groq`: Integration with Groq AI models
- `python-dotenv`: Environment variable management

## Model Information

This application uses the **LLaMA 3 70B** model from Groq, which provides:
- High-quality natural language understanding
- Efficient processing of structured data
- Detailed analytical responses

## Limitations

- Large CSV files may take longer to process
- The entire dataset is sent to the AI model for analysis
- API rate limits may apply based on your Groq plan

## Troubleshooting

### Common Issues

**"API key not found" error**
- Ensure your `.env` file is in the correct directory
- Verify your Groq API key is valid and properly formatted

**File upload issues**
- Check that your file is a valid CSV format
- Ensure the file size is within reasonable limits
- Verify the CSV has proper headers

**Slow responses**
- Large datasets may take time to process
- Consider using smaller sample datasets for testing

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them publicly
- The application sends your data to Groq's servers for processing


## Example Questions to Try

Once you've uploaded your CSV, try asking these types of questions:

- **Statistical Analysis**: "What are the mean, median, and mode of the sales column?"
- **Data Quality**: "Are there any missing values in the dataset?"
- **Trends**: "What patterns do you notice in the data over time?"
- **Comparisons**: "Compare the performance between different categories"
- **Summaries**: "Give me a summary of the key insights from this data"
