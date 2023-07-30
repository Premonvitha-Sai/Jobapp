import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Function to load the dataset
def load_data():
    df = pd.read_csv('data.csv')
    return df

# Function to drop unnecessary columns
def drop_columns(df):
    df.drop(['Uniq Id','Crawl Timestamp'], axis=1, inplace=True)
    return df

# Function to print the information about the dataset
def print_info(df):
    info = df.info()
    return info

# Function to print the shape of the dataset
def print_shape(df):
    shape = df.shape
    return shape

# Function to calculate the percentage of missing values
def missing_values(df):
    missing_percentage = df.isnull().sum()*100/len(df)
    return missing_percentage

# Function to identify duplicate entries
def print_duplicates(df):
    duplicates = df[df.duplicated(keep=False)]
    return duplicates

# Main function to control the flow of the application
def main():
    st.sidebar.title("Choose Here!!!")
    selection = st.sidebar.radio("Go to", ["Home", "Data Overview", "Visualizations", "Search for Jobs"])

    # Load processed data for visualizations and search
    data = pd.read_csv('processed_data.csv')

    if selection == "Home":
        st.title('Job Search App')
        st.image('image1.jpg', caption='Job Search')
        st.write('Developed By:')
        st.write('Swapna Dande')
        st.write('Premonvitha Sai Rayana')
        st.write('@ Research and Analysis Interns')

    elif selection == "Data Overview":
        st.title('Data Overview')

        # Load and preprocess data
        df = load_data()
        df = drop_columns(df)

        # Print info and shape of the dataset
        info = print_info(df)
        st.write(info)

        shape = print_shape(df)
        st.write(f'Shape of the dataset: {shape}')

        # Print duplicate entries and percentage of missing values
        duplicates = print_duplicates(df)
        st.write('Duplicate entries:')
        st.write(duplicates)

        st.write('Percentage of missing values:')
        missing_percentage = missing_values(df)
        st.write(missing_percentage)

    elif selection == "Visualizations":
        st.title('Visualizations')

        # Bar chart of unique value counts
        st.subheader('Number of Unique Values')
        unique_counts = data.nunique()
        st.bar_chart(unique_counts)

        # Horizontal bar plot of job salaries
        st.subheader('Job Salaries Plot')
        job_salary_counts = data['Job Salary'].value_counts().iloc[:10]
        fig1, ax1 = plt.subplots()
        ax1 = job_salary_counts.plot(kind='barh', colormap='Accent')
        plt.xlabel('No. of jobs')
        plt.ylabel('Salaries')
        st.pyplot(fig1)

        # Word cloud of key skills
        st.subheader('Word Cloud of Key Skills')
        common_words = ' '.join(data['Key Skills'].value_counts().index.ravel())
        wordcloud = WordCloud(width=1200, height=600, background_color='white', min_font_size=10).generate(common_words)
        fig2, ax2 = plt.subplots()
        ax2.imshow(wordcloud, interpolation='bilinear')
        ax2.axis('off')
        st.pyplot(fig2)

        # Bar charts of top 10 job titles with respective experience and salary
        st.subheader('Top 10 Popular Job Titles - Experience and Salary')
        for i in data['Job Title'].value_counts().index.tolist()[:10]:
            df = data[(data['Job Title'] == i) & (data['Job Salary'] != 'Not Disclosed by Recruiter')][['Job Salary','Job Experience Required']]
            fig = px.bar(df, x='Job Salary', y='Job Experience Required', color='Job Salary', height=400)
            st.plotly_chart(fig)

        # Sunburst chart of job salary and role category
        st.subheader('Sunburst Chart - Job Salary and Role Category')
        df1 = data[data['Job Salary'] != 'Not Disclosed by Recruiter'].sort_values('Job Salary',ascending=False)[['Job Salary','Role Category']]
        fig = px.sunburst(df1, path=['Role Category','Job Salary'])
        st.plotly_chart(fig)

        # Pie charts of job roles in top 10 locations
        st.subheader('Job Roles in Top 10 Locations')
        for i in data.Location.value_counts().index.tolist()[:10]:
            fig = px.pie(data[data.Location == i], names='Role Category', title = 'Job Roles in ' + i)
            st.plotly_chart(fig)

    elif selection == "Search for Jobs":
        st.title('Search for Jobs')
        st.image('image.jpg', caption='Job Search')
        search_term = st.text_input('Search by job title or keyword:')
        location = st.text_input('Location:')
        search_button = st.button('Search')

        # Search functionality
        if search_button:
            if search_term and location:
                filtered_data = data[
                    (data['Job Title'].str.contains(search_term, case=False)) &
                    (data['Location'].str.contains(location, case=False))
                ]
            elif search_term:
                filtered_data = data[
                    data['Job Title'].str.contains(search_term, case=False)
                ]
            elif location:
                filtered_data = data[
                    data['Location'].str.contains(location, case=False)
                ]
            else:
                filtered_data = None

            # Display the search results
            if filtered_data is not None and len(filtered_data) > 0:
                st.subheader(f'Found {len(filtered_data)} jobs')
                st.dataframe(filtered_data)
            elif filtered_data is not None:
                st.write('No jobs found based on the search criteria.')

if __name__ == "__main__":
    main()
