import streamlit as st
import pandas as pd
import numpy as np
import hmac

if __name__ == '__main__':

    st.title('OTIS Dashboard')
    st.write("This dashboard is a tool to explore the data scraped from the Michigan Department of Corrections Offender Tracking Information System (OTIS). Use the sidebar to filter the data, then explore the visualizations below. All tables can be downloaded. Contact noahattal@gmail.com for any questions or concerns.")

    url='https://drive.google.com/file/d/1QsGJ7LO5JwWFgqu-I_e54os9v-tf2nar/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]

    def check_password():
        """Returns `True` if the user had the correct password."""

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        # Return True if the password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
            )

        if "password_correct" in st.session_state:
            st.error("😕 Password incorrect")
        return False

    if not check_password():
        st.stop()  # Do not continue if check_password is not True.



    @st.cache_data
    def load_data():
        data = pd.read_csv(url)
        return data

    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text('')


    #Filtering

    #Status
    status_unique = data['valCurrentStatus'].unique().tolist()
    status_unique_all = status_unique.copy()
    status_unique_all.append('All')

    #Race
    race_unique = data['valRace'].unique().tolist()
    race_unique_all = race_unique.copy()
    race_unique_all.append('All')

    #Gender
    gender_unique = data['valGender'].unique().tolist()

    #County
    county_unique = data['County'].unique().tolist()
    county_unique_all = county_unique.copy()
    county_unique_all.append('All')

    #Life Sentences
    life_sentence_unique = data['life_sentence'].unique().tolist()

    #MCL
    mcl_unique = data['MCL#'].unique().tolist()
    mcl_unique_all = mcl_unique.copy()
    mcl_unique_all.append('All')

    #Crime Type
    crime_type_unique = data['crime_type'].unique().tolist()
    crime_type_unique_all = crime_type_unique.copy()
    crime_type_unique_all.append('All')

    #Location
    location_unique = data['valLocation'].unique().tolist()
    location_unique_all = location_unique.copy()
    location_unique_all.append('All')

    #SSL Elegible
    ssl_eligible_unique = data['SSL_category'].unique().tolist()



    #Sidebar
    st.sidebar.header("Select options from below:")
    status_select = st.sidebar.multiselect('Select Status:', status_unique_all, default='Prisoner')
    ssl_select = st.sidebar.multiselect('SLL Eligible:', ssl_eligible_unique, default=('Currently Eligible', 'Eligible in Next Ten Years', 'Not Eligible'))
    life_sentence_select = st.sidebar.multiselect('Life Sentence:', life_sentence_unique, default=life_sentence_unique)
    race_select = st.sidebar.multiselect('Select Race:', race_unique_all, default='All')
    gender_select = st.sidebar.multiselect('Select Gender:', gender_unique, default=('Male', 'Female'))
    county_select = st.sidebar.multiselect('Select County:', county_unique_all, default='All')
    mcl_select = st.sidebar.multiselect('Select MCL:', mcl_unique_all, default='All')
    crime_type_select = st.sidebar.multiselect('Select Crime Type:', crime_type_unique_all, default='All')
    location_select = st.sidebar.multiselect('Select Location:', location_unique_all, default='All')

    if "All" in status_select:
        status_select = status_unique
    if "All" in race_select:
        race_select = race_unique
    if "All" in county_select:
        county_select = county_unique
    if "All" in mcl_select:
        mcl_select = mcl_unique
    if "All" in crime_type_select:
        crime_type_select = crime_type_unique
    if "All" in location_select:
        location_select = location_unique


    #Min and Max Date
    age_select = st.sidebar.slider('Current Age', 0, 100, (0, 100))
    age_at_offense	 = st.sidebar.slider('Age at Offense', 0, 100, (0, 100))
    time_served = st.sidebar.slider('Time Served', 0, 70, (0, 100))
    min_sentence = st.sidebar.slider('Min Sentence', 0, 100, (0, 100))
    max_sentence = st.sidebar.slider('Max Sentence', 0, 1000, (0, 1000))
    year_of_offense = st.sidebar.slider('Year of Offense', 1950, 2024, (1950, 2024))





    filtered_data = data[(data['valCurrentStatus'].isin(status_select)) \
                        & (data['SSL_category'].isin(ssl_select)) \
                        & (data['valRace'].isin(race_select)) \
                        & (data['valGender'].isin(gender_select)) \
                        & (data['County'].isin(county_select)) \
                        & (data['life_sentence'].isin(life_sentence_select)) \
                        & (data['MCL#'].isin(mcl_select)) \
                        & (data['crime_type'].isin(crime_type_select)) \
                        & (data['valLocation'].isin(location_select)) \
                        & (data['current_age'].between(age_select[0], age_select[1])) \
                        & (data['time_served'].between(time_served[0], time_served[1])) \
                        & (data['min_sentence_years'].between(min_sentence[0], min_sentence[1]) | (data['min_sentence_years'] == np.inf)) \
                        & (data['max_sentence_years'].between(max_sentence[0], max_sentence[1]) | (data['max_sentence_years'] == np.inf)) \
                        & (data['year_of_offense'].between(year_of_offense[0], year_of_offense[1])) \
                        & (data['age_at_offense'].between(age_at_offense[0], age_at_offense[1]))]



    ############### Front End ###############


    # Scrape date
    st.write('Scrape Date (dd/mm/yyyy): 01-06-2025')

    #Add Spacer
    st.write('')

    if st.checkbox('Show/Download Raw Web Scrape'):
        st.subheader('Raw data')
        st.write(data)


    if st.checkbox('Show/Download Filtered data'):
        st.subheader('Filtered Data')
        st.write(filtered_data)

    #Add Spacer
    st.divider()


    # Display total individuals with comma formatting
    st.metric('Total (Filtered) Individuals:', "{:,}".format(filtered_data.shape[0]))


    # Use columns for side-by-side display of charts
    col1, col2 = st.columns(2)

    # Race/Ethnicity Distribution
    with col1:
    # Calculate the percentage column for race/ethnicity distribution
        total_race = filtered_data['valRace'].shape[0]
        bargraph_race = filtered_data['valRace'].value_counts().reset_index()
        bargraph_race.columns = ['Race', 'Count']
        bargraph_race['Percentage (%)'] = ((bargraph_race['Count'] / total_race) * 100).round(2)

        # Display bar chart for race/ethnicity distribution using st.bar_chart
        st.subheader('Race/Ethnicity')
        if st.checkbox('Show Race/Ethnicity Table'):
            st.write('Race/Ethnicity Table', bargraph_race)
        st.bar_chart(bargraph_race[['Race', 'Count']].set_index('Race'))



    # Gender Distribution
    with col2:
        total_gender = filtered_data['valGender'].shape[0]
        bargraph_gender = filtered_data['valGender'].value_counts().reset_index()
        bargraph_gender.columns = ['Gender', 'Count']
        bargraph_gender['Percentage (%)'] = ((bargraph_gender['Count'] / total_gender) * 100).round(2)

        #Display bar chart for gender distribution using st.bar_chart
        st.subheader('Gender')
        if st.checkbox('Show Gender Table'):
            st.write('Gender Table', bargraph_gender)
        st.bar_chart(bargraph_gender[['Gender', 'Count']].set_index('Gender'))


    # Use columns for side-by-side display of charts
    col3, col4 = st.columns(2)

    # Age Distribution
    with col3:
        total_age = filtered_data['current_age'].shape[0]
        bargraph_age = filtered_data['current_age'].value_counts().reset_index()
        bargraph_age.columns = ['Age', 'Count']
        bargraph_age['Percentage (%)'] = ((bargraph_age['Count'] / total_age) * 100).round(2)

        # Display bar chart for age distribution using st.bar_chart
        st.subheader('Age')
        if st.checkbox('Show Age Table'):
            st.write('Age Table', bargraph_age)
        if st.checkbox('Show Age Stats'):
            st.write('Age Stats', filtered_data['current_age'].describe())
        st.bar_chart(bargraph_age[['Age', 'Count']].set_index('Age'))



    # Time Served Distribution
    with col4:
        total_time_served = filtered_data['time_served'].shape[0]
        bargraph_time_served = filtered_data['time_served'].value_counts().reset_index()
        bargraph_time_served.columns = ['Time Served', 'Count']
        bargraph_time_served['Percentage (%)'] = ((bargraph_time_served['Count'] / total_time_served) * 100).round(2)

        # Display bar chart for time served distribution using st.bar_chart
        st.subheader('Time Served')
        if st.checkbox('Show Time Served Table'):
            st.write('Time Served Table', bargraph_time_served)
        if st.checkbox('Show Time Served Stats'):
            st.write('Time Served Stats', filtered_data['time_served'].describe())
        st.bar_chart(bargraph_time_served[['Time Served', 'Count']].set_index('Time Served'))



    # Use columns for side-by-side display of charts
    col5, col6 = st.columns(2)

    # Min Sentence Distribution
    with col5:
        #Clump min sentence years into bins
        bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 101, np.inf]
        labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-100', 'Life']
        filtered_data['min_sentence_years_cat'] = pd.cut(filtered_data['min_sentence_years'], bins=bins, labels=labels, include_lowest=True)

        total_min_sentence = filtered_data['min_sentence_years_cat'].shape[0]
        bargraph_min_sentence = filtered_data['min_sentence_years_cat'].value_counts().reset_index()
        bargraph_min_sentence.columns = ['Min Sentence', 'Count']
        bargraph_min_sentence['Percentage (%)'] = ((bargraph_min_sentence['Count'] / total_min_sentence) * 100).round(2)

        # Display bar chart for min sentence distribution using st.bar_chart
        st.subheader('Min Sentence')
        if st.checkbox('Show Min Sentence Table'):
            st.write('Min Sentence Table', bargraph_min_sentence)
        st.bar_chart(bargraph_min_sentence[['Min Sentence', 'Count']].set_index('Min Sentence'))
        st.write('*Note: Bins are lower bounded (i.e. 0-5 includes 0 but not 5).')




    # County bargraph (top ten) with percentages
    with col6:
        total_county = filtered_data['County'].shape[0]
        bargraph_county = filtered_data['County'].value_counts().reset_index()
        bargraph_county.columns = ['County', 'Count']
        bargraph_county['Percentage (%)'] = ((bargraph_county['Count'] / total_county) * 100).round(2)
        bargraph_county_ten = bargraph_county.sort_values(by='Count', ascending=False).head(10)

        # Display bar chart for county distribution using st.bar_chart
        st.subheader('County')
        if st.checkbox('Show County Table'):
            st.write('County Table', bargraph_county)
        st.bar_chart(bargraph_county_ten[['County', 'Count']].set_index('County').sort_index(ascending=False))
        st.write('*Note: Only the top ten counties are displayed. Table has full list.')

    # Use columns for side-by-side display of charts
    col7, col8 = st.columns(2)

    # Crime Type Distribution
    with col7:
        total_crime_type = filtered_data['crime_type'].shape[0]
        bargraph_crime_type = filtered_data['crime_type'].value_counts().reset_index()
        bargraph_crime_type.columns = ['Crime Type', 'Count']
        bargraph_crime_type['Percentage (%)'] = ((bargraph_crime_type['Count'] / total_crime_type) * 100).round(2)

        # Display bar chart for crime type distribution using st.bar_chart
        st.subheader('Crime Type')
        if st.checkbox('Show Crime Type Table'):
            st.write('Crime Type Table', bargraph_crime_type)
        st.bar_chart(bargraph_crime_type[['Crime Type', 'Count']].set_index('Crime Type'))


    #  st.subheader('County Distribution')
    #     county_table = filtered_data['County'].value_counts().reset_index()
    #     county_table.columns = ['County', 'Count']
    #     county_table['Percentage (%)'] = ((county_table['Count'] / county_table['Count'].sum()) * 100).round(2)
    #     st.write('County Table', county_table)

