import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import jira_functions as jira_functions

issues = jira_functions.get_my_issue_worklogs()

def main():
    st.set_page_config(layout="wide")
    
    # Initialize session state for week offset if it doesn't exist
    if 'week_offset' not in st.session_state:
        st.session_state.week_offset = 0

    # Add navigation buttons in a horizontal layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Previous Week"):
            st.session_state.week_offset -= 1
    with col2:
        st.write("") # Empty space for centering
    with col3:
        if st.button("Next Week →"):
            st.session_state.week_offset += 1

    # Calculate dates based on week offset
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=st.session_state.week_offset)
    dates = [(start_of_week + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(5)]

    #distinct_parents = list(set(issue['parent'] for issue in issues if 'parent' in issue))
    
    # Rest of your existing data processing code
    data = []
    for issue in issues:
        row = {
            'Issue': f"{issue['key']} - {issue['summary']}"
        }
        
        for date in dates:
            row[date] = 0
            
        for worklog in issue['worklogs']:
            worklog_date = datetime.strptime(worklog['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')        
            if worklog_date in dates:
                row[worklog_date] += worklog['timeSpentSeconds'] / 3600
                
        data.append(row)
    
    df = pd.DataFrame(data)
    print_page(df, dates, data)

def print_page(df, dates, data):
    st.title("Jira Worklog Dashboard")
    print_daily_totals(df, dates)
    print_issue_list(df, dates)
    add_hours_form(data, dates)

def print_issue_list(df, dates):
    # Create an empty DataFrame with the required columns
    st.subheader("Issues list and hours logged")
    columns = ['Issue'] + dates
    print("Columns  ", columns)
    df = pd.DataFrame(columns=columns)
    df['Issue'] = df['Issue'].astype('string')
    df[dates] = df[dates].astype('float64')

    # Map the dates to weekday columns
    # date_to_day = dict(zip(dates, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
    # print("date_to_day  ", date_to_day)

    # Add rows one by one
    for issue in issues:
        new_row = {
            'Issue': f"{issue['key']} - {issue['summary']}"
        }
        
        # Initialize all dates with 0.0
        for date in dates:
            new_row[date] = 0.0
        
        # Fill in logged hours
        for worklog in issue['worklogs']:
            worklog_date = datetime.strptime(worklog['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')        
            if worklog_date in dates:
                new_row[worklog_date] += worklog['timeSpentSeconds'] / 3600
                
        # Append the row to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    st.dataframe(df, hide_index=True)
    #st.write(df.to_html(escape=False), unsafe_allow_html=True)

# Display daily totals
def print_daily_totals(df, dates):
    daily_totals = df[dates].sum()
    st.subheader("Daily Totals (Hours)")
    st.dataframe(pd.DataFrame([daily_totals], index=['Total']),
                column_config={
                    col: st.column_config.NumberColumn(width="small") for col in daily_totals.index
                    })

# Add hours form
def add_hours_form(data, dates):
    st.subheader("Log Hours")
    selected_issue = st.selectbox("Select Issue", [row['Issue'] for row in data])
    selected_date = st.selectbox("Select Date", dates)
    hours = st.number_input("Hours", min_value=0.0, max_value=24.0, step=0.5)

    if st.button("Log Hours"):
        issue_key = selected_issue.split(" - ")[0]
        st.success(f"Logged {hours} hours for {issue_key} on {selected_date}")
        jira_functions.add_time(issue_key, f"{hours}h")

main()