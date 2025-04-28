# basic_data_agent.py
import pandas as pd
import re
import numpy as np

class CustomCSVDataAgent:
    def __init__(self):
        """Initialize the Custom CSV Data Agent."""
        self.df = None
        self.file_path = None
        
    def load_csv(self, file_path):
        """Load a CSV file into a pandas DataFrame."""
        try:
            self.file_path = file_path
            self.df = pd.read_csv(file_path)
            return f"Successfully loaded CSV with {len(self.df)} rows and {len(self.df.columns)} columns."
        except Exception as e:
            return f"Error loading CSV: {str(e)}"
    
    def process_query(self, query):
        """Process natural language queries and return appropriate responses."""
        if self.df is None:
            return "No CSV file loaded. Please load a CSV file first."
        
        query = query.lower().strip()
        
        # Basic dataset information
        if re.search(r"how many (rows|records|entries|items|data points)", query):
            return f"The dataset contains {len(self.df)} records."
        
        if re.search(r"(what|which|list|show) (are the |the )?(columns|fields)", query):
            columns = list(self.df.columns)
            return f"The dataset contains {len(columns)} columns:\n" + "\n".join([f"- {col}" for col in columns])
        
        # Summary statistics
        if "summary" in query or "describe" in query or "statistics" in query:
            col_match = re.search(r"(summary|describe|statistics|stats) (of|for) (.+?)(\?|$)", query)
            if col_match:
                col_name = self._find_closest_column(col_match.group(3).strip())
                if col_name:
                    return self._get_column_stats(col_name)
            # General dataset summary
            numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
            if len(numeric_cols) > 0:
                summary = self.df[numeric_cols].describe().round(2).to_string()
                return f"Summary statistics for numeric columns:\n{summary}"
            return "No numeric columns found in the dataset."
        
        # Top/Bottom values
        top_match = re.search(r"(top|highest|maximum|max|largest) (\d+)? ?(.+?)(\?|$|\s+in)", query)
        if top_match:
            n = int(top_match.group(2)) if top_match.group(2) else 5
            col_name = self._find_closest_column(top_match.group(3).strip())
            if col_name:
                return self._get_top_values(col_name, n)
        
        bottom_match = re.search(r"(bottom|lowest|minimum|min|smallest) (\d+)? ?(.+?)(\?|$|\s+in)", query)
        if bottom_match:
            n = int(bottom_match.group(2)) if bottom_match.group(2) else 5
            col_name = self._find_closest_column(bottom_match.group(3).strip())
            if col_name:
                return self._get_bottom_values(col_name, n)
        
        # Average/Mean/Median values
        avg_match = re.search(r"(average|mean|median|avg) (.+?)(\?|$|\s+in|\s+of)", query)
        if avg_match:
            col_name = self._find_closest_column(avg_match.group(2).strip())
            if col_name and pd.api.types.is_numeric_dtype(self.df[col_name]):
                if "median" in query:
                    return f"Median {col_name}: {self.df[col_name].median()}"
                else:
                    return f"Average {col_name}: {self.df[col_name].mean():.2f}"
            elif col_name:
                return f"{col_name} is not numeric, cannot calculate average."
        
        # Distribution of values
        dist_match = re.search(r"(distribution|breakdown|count) (of|by) (.+?)(\?|$)", query)
        if dist_match:
            col_name = self._find_closest_column(dist_match.group(3).strip())
            if col_name:
                return self._get_distribution(col_name)
        
        # Correlation/relationship between columns
        corr_match = re.search(r"(correlation|relationship) between (.+?) and (.+?)(\?|$)", query)
        if corr_match:
            col1 = self._find_closest_column(corr_match.group(2).strip())
            col2 = self._find_closest_column(corr_match.group(3).strip())
            if col1 and col2 and pd.api.types.is_numeric_dtype(self.df[col1]) and pd.api.types.is_numeric_dtype(self.df[col2]):
                corr = self.df[col1].corr(self.df[col2])
                return f"Correlation between {col1} and {col2}: {corr:.3f}"
            elif col1 and col2:
                return f"Cannot calculate correlation between non-numeric columns: {col1} and {col2}"
        
        # Filter data
        filter_match = re.search(r"(where|with|having) (.+?) (is|equals|=|==|>|<|>=|<=|!=) (.+?)(\?|$)", query)
        if filter_match:
            col_name = self._find_closest_column(filter_match.group(2).strip())
            operator = filter_match.group(3).strip()
            value = filter_match.group(4).strip().replace("'", "").replace('"', '')
            
            if col_name:
                return self._filter_data(col_name, operator, value)
        
        # Unique values
        unique_match = re.search(r"(unique|distinct) (.+?)(\?|$|\s+in|\s+of)", query)
        if unique_match:
            col_name = self._find_closest_column(unique_match.group(2).strip())
            if col_name:
                unique_count = self.df[col_name].nunique()
                return f"There are {unique_count} unique values in {col_name}."
        
        # Missing values
        if "missing" in query or "null" in query:
            col_name = None
            for col in self.df.columns:
                if col.lower() in query:
                    col_name = col
                    break
            
            if col_name:
                missing_count = self.df[col_name].isna().sum()
                return f"Column {col_name} has {missing_count} missing values ({missing_count/len(self.df)*100:.1f}%)."
            else:
                # Check all columns
                missing_data = self.df.isna().sum()
                missing_cols = missing_data[missing_data > 0]
                if len(missing_cols) == 0:
                    return "There are no missing values in the dataset."
                else:
                    result = "Missing values by column:\n"
                    for col, count in missing_cols.items():
                        result += f"- {col}: {count} ({count/len(self.df)*100:.1f}%)\n"
                    return result
        
        # Recommended products/items
        if "recommended" in query or "recommendation" in query:
            if "Recommendation" in self.df.columns:
                recommended_count = self.df[self.df["Recommendation"] == 1].shape[0]
                total = len(self.df)
                return f"There are {recommended_count} recommended items out of {total} ({recommended_count/total*100:.1f}%)."
        
        # Highest/top rated
        if ("highest rated" in query or "top rated" in query) and "Rating" in self.df.columns:
            n = 5  # Default to top 5
            n_match = re.search(r"top (\d+)", query)
            if n_match:
                n = int(n_match.group(1))
            return self._get_top_values("Rating", n)
        
        # Common style query for dress dataset
        if "style" in query and "Style" in self.df.columns:
            return self._get_distribution("Style")
            
        # If no specific pattern matched, try to find column mentions
        for col in self.df.columns:
            if col.lower() in query:
                return self._get_column_info(col)
        
        # Fall back to generic response
        return (f"I couldn't understand your query. Try asking about columns, statistics, or distributions. "
                f"For example: 'Show me all columns', 'What's the average of [column]?', or 'Distribution of [column]'")
    
    def _find_closest_column(self, col_query):
        """Find the closest matching column from the query."""
        col_query = col_query.lower()
        
        # Direct match
        for col in self.df.columns:
            if col.lower() == col_query:
                return col
        
        # Partial match
        for col in self.df.columns:
            if col_query in col.lower() or col.lower() in col_query:
                return col
        
        return None
    
    def _get_column_stats(self, column):
        """Get basic statistics for a specified column."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        col_data = self.df[column]
        result = f"Statistics for {column}:\n"
        
        if pd.api.types.is_numeric_dtype(col_data):
            stats = col_data.describe().round(2)
            for stat, value in stats.items():
                result += f"- {stat}: {value}\n"
        else:
            unique_count = col_data.nunique()
            most_common = col_data.value_counts().head(1).to_dict()
            result += f"- count: {col_data.count()}\n"
            result += f"- unique values: {unique_count}\n"
            for val, count in most_common.items():
                result += f"- most common: {val} ({count} occurrences)\n"
        
        return result
    
    def _get_top_values(self, column, n=5):
        """Get top N values for a column."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        if pd.api.types.is_numeric_dtype(self.df[column]):
            # For numeric columns, get highest values
            top_values = self.df.nlargest(n, column)
            result = f"Top {n} highest values in {column}:\n"
            for i, (idx, row) in enumerate(top_values.iterrows(), 1):
                result += f"{i}. {row[column]}\n"
        else:
            # For categorical columns, get most frequent values
            value_counts = self.df[column].value_counts().head(n)
            result = f"Top {n} most frequent values in {column}:\n"
            for i, (value, count) in enumerate(value_counts.items(), 1):
                result += f"{i}. {value}: {count} occurrences\n"
        
        return result
    
    def _get_bottom_values(self, column, n=5):
        """Get bottom N values for a column."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        if pd.api.types.is_numeric_dtype(self.df[column]):
            # For numeric columns, get lowest values
            bottom_values = self.df.nsmallest(n, column)
            result = f"Bottom {n} lowest values in {column}:\n"
            for i, (idx, row) in enumerate(bottom_values.iterrows(), 1):
                result += f"{i}. {row[column]}\n"
        else:
            # For categorical columns, get least frequent values
            value_counts = self.df[column].value_counts().tail(n)
            result = f"Least {n} frequent values in {column}:\n"
            for i, (value, count) in enumerate(value_counts.items(), 1):
                result += f"{i}. {value}: {count} occurrences\n"
        
        return result
    
    def _get_distribution(self, column):
        """Get distribution of values in a column."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        value_counts = self.df[column].value_counts().head(10)
        total = len(self.df)
        
        result = f"Distribution of values in {column} (top 10):\n"
        for value, count in value_counts.items():
            percentage = count / total * 100
            result += f"- {value}: {count} ({percentage:.1f}%)\n"
        
        if self.df[column].nunique() > 10:
            result += f"... and {self.df[column].nunique() - 10} more unique values"
        
        return result
    
    def _filter_data(self, column, operator, value):
        """Filter data based on a condition."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        # Convert value to appropriate type
        try:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                value = float(value)
            elif value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
        except ValueError:
            pass
        
        # Apply filter
        if operator in ['is', 'equals', '=', '==']:
            filtered = self.df[self.df[column] == value]
        elif operator == '>':
            filtered = self.df[self.df[column] > value]
        elif operator == '<':
            filtered = self.df[self.df[column] < value]
        elif operator == '>=':
            filtered = self.df[self.df[column] >= value]
        elif operator == '<=':
            filtered = self.df[self.df[column] <= value]
        elif operator in ['!=', 'not equals', 'is not']:
            filtered = self.df[self.df[column] != value]
        else:
            return f"Unsupported operator: {operator}"
        
        result = f"Found {len(filtered)} records where {column} {operator} {value}.\n"
        
        if len(filtered) > 0 and len(filtered) <= 5:
            # Show all results if 5 or fewer
            sample_cols = list(filtered.columns)[:5] if len(filtered.columns) > 5 else filtered.columns
            result += filtered[sample_cols].to_string()
        elif len(filtered) > 5:
            # Show first 5 results if more
            sample_cols = list(filtered.columns)[:5] if len(filtered.columns) > 5 else filtered.columns
            result += filtered[sample_cols].head(5).to_string()
            result += "\n... (showing 5 of " + str(len(filtered)) + " results)"
        
        return result
    
    def _get_column_info(self, column):
        """Get general information about a column."""
        if column not in self.df.columns:
            return f"Column '{column}' not found."
        
        result = f"Information about column '{column}':\n"
        result += f"- Data type: {self.df[column].dtype}\n"
        result += f"- Non-null values: {self.df[column].count()} out of {len(self.df)}\n"
        result += f"- Unique values: {self.df[column].nunique()}\n"
        
        if pd.api.types.is_numeric_dtype(self.df[column]):
            result += f"- Min: {self.df[column].min()}\n"
            result += f"- Max: {self.df[column].max()}\n"
            result += f"- Mean: {self.df[column].mean():.2f}\n"
            result += f"- Median: {self.df[column].median()}\n"
        else:
            # Show most common values for non-numeric columns
            most_common = self.df[column].value_counts().head(3)
            result += "- Most common values:\n"
            for value, count in most_common.items():
                result += f"  * {value}: {count} occurrences\n"
        
        return result