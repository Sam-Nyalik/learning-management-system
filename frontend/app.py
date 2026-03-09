import streamlit as st
import requests

# FastAPI Backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Workbook System", layout="wide", initial_sidebar_state="expanded")

# --- Styling ---
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 5px;
        height: 2.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialisation ---
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# --- Persist session across refreshes using query params ---
params = st.query_params
if st.session_state.token is None and "token" in params:
    st.session_state.token = params["token"]

# --- Helpers ---
def api_request(method, endpoint, json=None, params=None):
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    url = f"{BACKEND_URL}{endpoint}"
    try:
        response = requests.request(method, url, json=json, params=params, headers=headers)
        return response
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def do_login(email, password):
    resp = api_request("POST", "/auth/login", json={"email": email, "password": password})
    if resp and resp.status_code == 200:
        token = resp.json().get("access_token")
        st.session_state.token = token
        # Persist token in URL so it survives refresh
        st.query_params["token"] = token
        # Fetch user info
        user_resp = api_request("GET", "/auth/me")
        if user_resp and user_resp.status_code == 200:
            st.session_state.user = user_resp.json()
            return True
    return False

def do_logout():
    st.session_state.token = None
    st.session_state.user = None
    st.query_params.clear()
    st.rerun()

# --- Auth Pages ---
def login_register():
    st.title("Welcome to Workbook System")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            if do_login(email, password):
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials or server error")

    with tab2:
        st.subheader("Sign Up")
        reg_name = st.text_input("Full Name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        reg_role = st.selectbox("Role", ["student", "teacher", "director"])
        if st.button("Register"):
            payload = {"name": reg_name, "email": reg_email, "password": reg_pass, "role": reg_role}
            resp = api_request("POST", "/auth/signup", json=payload)
            if resp and resp.status_code == 200:
                st.success("Registration successful! Please login.")
            else:
                detail = resp.json().get("detail", "Unknown error") if resp else "No response"
                st.error(f"Registration failed: {detail}")

# --- Dashboard ---
def main_dashboard():
    user = st.session_state.user
    st.sidebar.title(f"Hi, {user['name']}!")
    st.sidebar.info(f"Role: {user['role'].capitalize()}")
    if st.sidebar.button("Logout"):
        do_logout()

    if user["role"] == "director":
        director_view()
    elif user["role"] == "teacher":
        teacher_view()
    elif user["role"] == "student":
        student_view()

# --- Director View ---
def director_view():
    st.header("Director Dashboard")
    tab_manage, tab_grades = st.tabs(["Manage Workbooks", "View Grades"])

    with tab_manage:
        with st.expander("Create New Workbook"):
            title = st.text_input("Workbook Title")
            if st.button("Create Workbook"):
                resp = api_request("POST", "/workbooks/", json={"title": title})
                if resp and resp.status_code == 200:
                    st.success("Workbook created!")
                    st.rerun()
                else:
                    st.error(f"Failed: {resp.json() if resp else 'No response'}")

        st.subheader("Workbooks & Worksheets")
        resp = api_request("GET", "/workbooks/")
        if resp and resp.status_code == 200:
            workbooks = resp.json()
            if not workbooks:
                st.info("No workbooks yet. Create one above.")
            for wb in workbooks:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.write(f"### {wb['title']}")
                        st.write(f"ID: {wb['id']}")
                    with col2:
                        ws_title = st.text_input("New Worksheet Title", key=f"ws_t_{wb['id']}")
                        if st.button("Add Worksheet", key=f"ws_b_{wb['id']}"):
                            ws_resp = api_request("POST", "/worksheets/", json={"title": ws_title, "workbook_id": wb['id']})
                            if ws_resp and ws_resp.status_code == 200:
                                st.success("Worksheet added!")
                                st.rerun()
                            else:
                                st.error(f"Failed: {ws_resp.json() if ws_resp else 'No response'}")

                    ws_list_resp = api_request("GET", f"/worksheets/{wb['id']}")
                    if ws_list_resp and ws_list_resp.status_code == 200:
                        worksheets = ws_list_resp.json()
                        if worksheets:
                            st.write("---")
                            for ws in worksheets:
                                st.write(f"{ws['title']} (ID: {ws['id']})")

    with tab_grades:
        st.subheader("Student Grades Report")
        resp = api_request("GET", "/grades/report")
        if resp is None:
            st.error("Could not connect to server.")
        elif resp.status_code == 403:
            st.error("Access denied.")
        elif resp.status_code != 200:
            st.error(f"Server error {resp.status_code}: {resp.text}")
        else:
            report = resp.json()
            if not report:
                st.info("No grades available yet. Students need to submit answers and teachers need to grade them.")
            else:
                for wb in report:
                    st.markdown(f"## {wb['workbook_title']}")
                    for ws in wb["worksheets"]:
                        with st.expander(f"{ws['worksheet_title']}"):
                            grades = ws["grades"]
                            if not grades:
                                st.info("No graded submissions in this worksheet.")
                            else:
                                for g in grades:
                                    with st.container(border=True):
                                        col1, col2, col3 = st.columns([3, 1, 1])
                                        with col1:
                                            st.write(f"**Q:** {g['question']}")
                                            st.write(f"**Answer:** {g['answer']}")
                                            st.write(f"**Student:** {g['student']}")
                                        with col2:
                                            st.metric("Grade", f"{g['grade']}/100")
                                            if g['feedback']:
                                                st.caption(f"{g['feedback']}")
                                        with col3:
                                            status_label = "Approved" if g['approved'] else "Not Approved"
                                            st.write(f"**{status_label}**")
                                            btn_col1, btn_col2 = st.columns(2)
                                            with btn_col1:
                                                if st.button("Approve", key=f"approve_{g['grade_id']}",
                                                             disabled=g['approved']):
                                                    apr_resp = api_request("PATCH", f"/grades/{g['grade_id']}/approve")
                                                    if apr_resp and apr_resp.status_code == 200:
                                                        st.rerun()
                                            with btn_col2:
                                                if st.button("Reject", key=f"reject_{g['grade_id']}",
                                                             disabled=not g['approved']):
                                                    rej_resp = api_request("PATCH", f"/grades/{g['grade_id']}/reject")
                                                    if rej_resp and rej_resp.status_code == 200:
                                                        st.rerun()




# --- Teacher View ---

def teacher_view():
    st.header("Teacher Dashboard")
    tab_questions, tab_grades = st.tabs(["Manage Questions", "Grade Answers"])

    with tab_questions:
        st.subheader("Add Question")
        wb_resp = api_request("GET", "/workbooks/")
        if wb_resp and wb_resp.status_code == 200:
            workbooks = wb_resp.json()
            if not workbooks:
                st.warning("No workbooks available.")
            else:
                wb_options = {wb['title']: wb['id'] for wb in workbooks}
                selected_wb = st.selectbox("Select Workbook", list(wb_options.keys()))
                if selected_wb:
                    ws_resp = api_request("GET", f"/worksheets/{wb_options[selected_wb]}")
                    if ws_resp and ws_resp.status_code == 200:
                        worksheets = ws_resp.json()
                        ws_options = {ws['title']: ws['id'] for ws in worksheets}
                        if ws_options:
                            selected_ws = st.selectbox("Select Worksheet", list(ws_options.keys()))
                            q_text = st.text_area("Question Text")
                            if st.button("Add Question"):
                                resp = api_request("POST", "/questions/",
                                                   json={"question_text": q_text, "worksheet_id": ws_options[selected_ws]})
                                if resp and resp.status_code == 200:
                                    st.success("Question added!")
                                else:
                                    st.error(f"Failed: {resp.json() if resp else 'No response'}")
                        else:
                            st.warning("No worksheets in this workbook. Ask a Director to add one.")

    with tab_grades:
        st.subheader("Student Submissions")
        resp = api_request("GET", "/answers/all")
        if resp is None:
            st.error("Could not connect to server.")
        elif resp.status_code == 403:
            st.error("Access denied. Make sure you are logged in as a teacher.")
        elif resp.status_code != 200:
            st.error(f"Server error {resp.status_code}: {resp.text}")
        else:
            answers = resp.json()
            if not answers:
                st.info("No student submissions yet.")
            else:
                for ans in answers:
                    with st.container(border=True):
                        # Fetch the related question text
                        q_resp = api_request("GET", f"/questions/by-id/{ans['question_id']}")
                        if q_resp and q_resp.status_code == 200:
                            q_text = q_resp.json().get("question_text", f"Question #{ans['question_id']}")
                        else:
                            q_text = f"Question #{ans['question_id']}"
                        st.write(f"**Q:** {q_text}")
                        st.write(f"**Answer:** {ans['answer_text']}")
                        st.caption(f"Student ID: {ans['student_id']} | Answer ID: {ans['id']}")
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            grade_val = st.number_input("Grade (0–100)", min_value=0, max_value=100,
                                                        step=1, key=f"grade_{ans['id']}")
                        with col2:
                            feedback_val = st.text_input("Feedback", key=f"fb_{ans['id']}")
                        if st.button("Submit Grade", key=f"grade_btn_{ans['id']}"):
                            grade_resp = api_request("POST", f"/grades/{ans['id']}",
                                                     params={"grade_value": grade_val, "feedback": feedback_val})
                            if grade_resp and grade_resp.status_code == 200:
                                st.success("Grade submitted!")
                            else:
                                st.error(f"Failed: {grade_resp.json() if grade_resp else 'No response'}")

# --- Student View ---
def student_view():
    st.header("Student Dashboard")

    # Initialise session state for loaded questions
    if "loaded_questions" not in st.session_state:
        st.session_state.loaded_questions = []
    if "loaded_ws_id" not in st.session_state:
        st.session_state.loaded_ws_id = None

    wb_resp = api_request("GET", "/workbooks/")
    if wb_resp and wb_resp.status_code == 200:
        workbooks = wb_resp.json()
        if not workbooks:
            st.info("No workbooks available yet.")
        else:
            wb_options = {wb['title']: wb['id'] for wb in workbooks}
            selected_wb = st.selectbox("Select Workbook", list(wb_options.keys()))
            if selected_wb:
                ws_resp = api_request("GET", f"/worksheets/{wb_options[selected_wb]}")
                if ws_resp and ws_resp.status_code == 200:
                    worksheets = ws_resp.json()
                    ws_options = {ws['title']: ws['id'] for ws in worksheets}
                    if ws_options:
                        selected_ws = st.selectbox("Select Worksheet", list(ws_options.keys()))
                        ws_id = ws_options[selected_ws]

                        if st.button("Load Questions"):
                            q_resp = api_request("GET", f"/questions/{ws_id}")
                            if q_resp and q_resp.status_code == 200:
                                st.session_state.loaded_questions = q_resp.json()
                                st.session_state.loaded_ws_id = ws_id
                            else:
                                st.error("Could not load questions.")

                        # Render questions from session state so they survive reruns
                        if st.session_state.loaded_questions and st.session_state.loaded_ws_id == ws_id:
                            if not st.session_state.loaded_questions:
                                st.info("No questions in this worksheet yet.")
                            for q in st.session_state.loaded_questions:
                                with st.container(border=True):
                                    st.write(f"**{q['question_text']}**")
                                    ans = st.text_area("Your Answer", key=f"ans_{q['id']}")
                                    if st.button("Submit Answer", key=f"btn_{q['id']}"):
                                        ans_resp = api_request("POST", "/answers/",
                                                               json={"question_id": q["id"], "answer_text": ans})
                                        if ans_resp and ans_resp.status_code == 200:
                                            st.success("Answer submitted!")
                                        else:
                                            detail = ans_resp.json().get("detail", "Unknown") if ans_resp else "No response"
                                            st.error(f"Failed: {detail}")
                    else:
                        st.info("No worksheets available in this workbook.")


# --- Main Entry ---
if not st.session_state.token:
    login_register()
else:
    # Load user info if missing (e.g. after refresh token restore)
    if not st.session_state.user:
        user_resp = api_request("GET", "/auth/me")
        if user_resp and user_resp.status_code == 200:
            st.session_state.user = user_resp.json()
        else:
            # Token is invalid/expired — clear and show login
            do_logout()
    if st.session_state.user:
        main_dashboard()
