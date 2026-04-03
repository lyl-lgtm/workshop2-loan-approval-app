import streamlit as st
from src.inference import get_prediction

st.set_page_config(
    page_title="Loan Approval Decision Support",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialise session state variables
if 'input_features' not in st.session_state:
    st.session_state['input_features'] = {}
if 'assessment' not in st.session_state:
    st.session_state['assessment'] = None


def _build_input_features(dep, ln_amt, ln_tm, cbl, rav):
    return {
        'dep': int(dep),
        'ln_amt': int(ln_amt),
        'ln_tm': int(ln_tm),
        'cbl': int(cbl),
        'rav': int(rav) * 1000,
    }


def app_sidebar():
    st.sidebar.header('Applicant Profile')
    st.sidebar.caption("Adjust the applicant details and run an instant assessment.")
    dep = st.sidebar.number_input("No. of Dependents", min_value=0, max_value=20, value=0, step=1)
    ln_amt = st.sidebar.number_input("Loan Amount '000s", min_value=0, value=100, step=1)
    ln_tm = st.sidebar.number_input("Loan Term", min_value=1, value=12, step=1)
    cbl = st.sidebar.number_input("CIBIL Score (300-900)", min_value=300, max_value=900, value=700, step=1)
    rav = st.sidebar.number_input("Residential Assets Value '000s", min_value=0, value=500, step=1)

    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Assess", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")
    if predict_button:
        st.session_state['input_features'] = _build_input_features(dep, ln_amt, ln_tm, cbl, rav)
        st.session_state['assessment'] = get_prediction(
            no_of_dependents=st.session_state['input_features']['dep'],
            loan_amount=st.session_state['input_features']['ln_amt'],
            loan_term=st.session_state['input_features']['ln_tm'],
            cibil_score=st.session_state['input_features']['cbl'],
            residential_assets_value=st.session_state['input_features']['rav'],
        )
    if reset_button:
        st.session_state['input_features'] = {}
        st.session_state['assessment'] = None
    return None


def app_body():
    st.title("Loan Approval Decision Support")
    st.caption("A Streamlit application that loads a trained machine learning model and returns an approval recommendation.")

    summary_col, metrics_col = st.columns([1.3, 1])

    with summary_col:
        st.subheader("How it works")
        st.write(
            "Use the sidebar to provide applicant details. The application applies the same preprocessing and trained model "
            "from the project pipeline, then returns an approval recommendation immediately."
        )
        st.write(
            "This demo is suitable for local testing now and for deployment to Streamlit Community Cloud once the repository "
            "is pushed to GitHub."
        )

    with metrics_col:
        st.subheader("Model Inputs")
        st.markdown("- Dependents")
        st.markdown("- Loan amount")
        st.markdown("- Loan term")
        st.markdown("- CIBIL score")
        st.markdown("- Residential assets value")

    st.divider()

    if st.session_state['input_features']:
        result_col, detail_col = st.columns([1, 1])

        with result_col:
            st.subheader("Decision")
            if st.session_state['assessment'] == 1:
                st.success("System assessment: Approved")
                st.metric("Recommendation", "Approved")
                st.progress(85)
                st.caption("The current applicant profile is assessed as favorable.")
            else:
                st.warning("System assessment: Rejected")
                st.metric("Recommendation", "Rejected")
                st.progress(35)
                st.caption("The current applicant profile is assessed as higher risk.")

        with detail_col:
            st.subheader("Submitted Inputs")
            st.json(st.session_state['input_features'])
    else:
        st.info("No assessment has been run yet. Enter applicant details in the sidebar and click `Assess`.")

    examples_col1, examples_col2 = st.columns(2)
    with examples_col1:
        st.subheader("Example: Likely Approved")
        st.code(
            "Dependents: 0\nLoan Amount ('000s): 100\nLoan Term: 12\nCIBIL Score: 800\nResidential Assets ('000s): 500"
        )
    with examples_col2:
        st.subheader("Example: Likely Rejected")
        st.code(
            "Dependents: 4\nLoan Amount ('000s): 20000\nLoan Term: 60\nCIBIL Score: 350\nResidential Assets ('000s): 10"
        )

    st.divider()
    st.caption("Built with Streamlit for Workshop II: local demo first, then GitHub + Streamlit Community Cloud deployment.")
    return None


def main():
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()
