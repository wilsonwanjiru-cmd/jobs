# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc
import requests
import json  # Add the json module for JSON error handling

base_url = "https://jobs.github.com/positions.json?description={}&location={}"

# Fxn to Retrieve Data
def get_data(url):
    resp = requests.get(url)

    # Check if the response status code indicates success
    if resp.status_code == 200:
        try:
            data = resp.json()
            return data
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON data: {e}")
            return None
    else:
        st.error(f"Failed to retrieve data. Status Code: {resp.status_code}")
        return None

JOB_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: #31333F;
  border-left: 5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h4>{}</h4>
<h5>{}</h5>
<h6>{}</h6>
</div>
"""

JOB_DES_HTML_TEMPLATE = """
<div style='color:#fff'>
{}
</div>
"""

def main():
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.title("DevDeeds - Search Jobs")

    if choice == "Home":
        st.subheader("Home")

        # Nav Search Form
        with st.form(key='searchform'):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                search_term = st.text_input("Search Job")

            with col2:
                location = st.text_input("Location")

            with col3:
                st.text("Search")
                submit_search = st.form_submit_button(label='Search')

        st.success("You searched for {} in {}".format(search_term, location))

        # Results
        if submit_search:
            # Create Search Query
            search_url = base_url.format(search_term, location)
            data = get_data(search_url)

            if data is not None:
                if len(data) > 0:
                    # Number of Results
                    num_of_results = len(data)
                    st.subheader("Showing {} jobs".format(num_of_results))

                    for i in data:
                        job_title = i['title']
                        job_location = i['location']
                        company = i['company']
                        company_url = i['company_url']
                        job_post_date = i['created_at']
                        job_desc = i['description']
                        job_howtoapply = i['how_to_apply']
                        st.markdown(JOB_HTML_TEMPLATE.format(job_title, company, job_location, job_post_date),
                                    unsafe_allow_html=True)

                        # Description
                        with st.expander("Description"):
                            stc.html(JOB_DES_HTML_TEMPLATE.format(job_desc), scrolling=True)

                        # How to Apply
                        with st.expander("How To Apply"):
                            stc.html(JOB_DES_HTML_TEMPLATE.format(job_howtoapply), scrolling=True)
                else:
                    st.warning("No jobs found for the given search criteria.")
            else:
                st.error("Failed to retrieve data. Check your search criteria or try again later.")

        with st.form(key='email_form'):
            st.write("Be the first to get new jobs info")
            email = st.text_input("Email")

            submit_email = st.form_submit_button(label='Subscribe')

            if submit_email:
                st.success("A message was sent to {}".format(email))

    else:
        st.subheader("About")

if __name__ == '__main__':
    main()
