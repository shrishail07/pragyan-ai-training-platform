# pragyan-ai-training-platform

before using the app run this query in supabase query for read and write access:

-- Allow the app to read and write to programs_running
CREATE POLICY "Allow public insert on programs_running" ON programs_running FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select on programs_running" ON programs_running FOR SELECT TO anon USING (true);

-- Allow the app to read and write to coordinators (to prevent this error on Tab 3)
CREATE POLICY "Allow public insert on coordinators" ON coordinators FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select on coordinators" ON coordinators FOR SELECT TO anon USING (true);


# PRAGYAN AI Training Platform

An end-to-end Streamlit application backed by a Supabase PostgreSQL database, designed to manage expert trainers, student enrollments, and academic coordinators for Pragyan AI.

The platform is divided into three role-based portals:

* **Admin Dashboard:** Manage planned/running programs, approve/reject trainer expressions of interest (EOIs), handle student custom requests, and assign classes to approved trainers.
* **Expert Trainer Portal:** Submit professional profiles, apply for training topics with expected pricing (EOI), and view assigned, approved class schedules.
* **Student Portal:** Create student profiles, request custom curriculum hours, accept Admin proposals, and enroll in planned programs.

## Tech Stack

* **Frontend/Backend:** Python, Streamlit (`streamlit>=1.32.0`)
* **Database:** Supabase (PostgreSQL)
* **Data Processing:** Pandas
* **API Client:** Supabase Python Client (`supabase>=2.31.0`)

---

## Deployment & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-repo/pragyan-ai-training-platform.git
cd pragyan-ai-training-platform

```


2. **Configure Streamlit Secrets:**
Create a `.streamlit/secrets.toml` file locally, or configure the Streamlit Community Cloud settings with your Supabase credentials:
```toml
# MUST be separated correctly to avoid API errors
SUPABASE_URL = "https://<your-project-id>.supabase.co"
SUPABASE_KEY = "eyJhbG..." # Your public anon key

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Run the App Locally:**
```bash
streamlit run app.py

```



---

## Database Configuration & Troubleshooting

If you encounter a `postgrest.exceptions.APIError` (specifically Code `42501` indicating a Row Level Security violation), it means your Streamlit app is attempting to write, read, or update a table that Supabase has locked down.

Run the SQL scripts below in your **Supabase SQL Editor** to resolve these database issues.

### 1. "Relation does not exist" or "Table not found"

**Issue:** The Streamlit app crashes upon startup or form submission because the required tables have not been created.
**Fix:** Run the master schema creation script.

```sql
CREATE TABLE programs_planned (id SERIAL PRIMARY KEY, name TEXT, skill_dept TEXT, duration_hrs INT, start_month TEXT, time_slot TEXT, price INT, seats_available INT, batch_size INT);
CREATE TABLE programs_running (id SERIAL PRIMARY KEY, name TEXT, duration TEXT, skills TEXT, class_link TEXT);
CREATE TABLE coordinators (id SERIAL PRIMARY KEY, program_name TEXT, name TEXT, email TEXT, phone TEXT, experience TEXT, cv_link TEXT, linkedin TEXT, github TEXT, emp_id TEXT);
CREATE TABLE trainer_profiles (id SERIAL PRIMARY KEY, name TEXT, email TEXT, skills TEXT, experience TEXT, linkedin TEXT, github TEXT, availability TEXT, status TEXT);
CREATE TABLE trainer_eoi (id SERIAL PRIMARY KEY, trainer_email TEXT, price INT, topic TEXT, time_slot TEXT, status TEXT);
CREATE TABLE trainer_classes (id SERIAL PRIMARY KEY, trainer_email TEXT, event_name TEXT, coordinator_name TEXT, date TEXT, time TEXT, attendance TEXT, completed TEXT, payment_status TEXT);
CREATE TABLE student_profiles (id SERIAL PRIMARY KEY, email TEXT, name TEXT, college TEXT, department TEXT, sem TEXT, marks_10th TEXT, marks_12th TEXT, cgpa FLOAT, dream_job TEXT, interested_skills TEXT);
CREATE TABLE student_custom_requests (id SERIAL PRIMARY KEY, student_email TEXT, request_details TEXT, status TEXT);
CREATE TABLE student_enrollments (id SERIAL PRIMARY KEY, student_email TEXT, program_id INT, status TEXT);

```

### 2. "New row violates row-level security policy" (Insert/Read Errors)

**Issue:** A user submits a form (e.g., Trainer Profile, Student Request, or Admin adding a running program), but Supabase rejects the `INSERT` operation.
**Fix:** Explicitly enable RLS and grant the `anon` public role permission to `INSERT` and `SELECT` (read/write).

```sql
-- Enable RLS universally
ALTER TABLE programs_planned ENABLE ROW LEVEL SECURITY;
ALTER TABLE programs_running ENABLE ROW LEVEL SECURITY;
ALTER TABLE coordinators ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainer_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainer_eoi ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainer_classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_custom_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_enrollments ENABLE ROW LEVEL SECURITY;

-- Grant baseline schema usage
GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;

-- Allow public INSERTS and SELECTS across all tables
CREATE POLICY "Allow public insert" ON programs_planned FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON programs_planned FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON programs_running FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON programs_running FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON coordinators FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON coordinators FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON trainer_profiles FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON trainer_profiles FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON trainer_eoi FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON trainer_eoi FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON trainer_classes FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON trainer_classes FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON student_profiles FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON student_profiles FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON student_custom_requests FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON student_custom_requests FOR SELECT TO anon USING (true);

CREATE POLICY "Allow public insert" ON student_enrollments FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public select" ON student_enrollments FOR SELECT TO anon USING (true);

```

### 3. Approvals fail to save (Update Errors)

**Issue:** Clicking "Approve" or "Reject" in the Admin dashboard triggers a success message in Streamlit, but the status remains "Pending" in the data table.
**Fix:** The database lacks an `UPDATE` policy. Run this query to allow the Streamlit app to modify existing rows.

```sql
CREATE POLICY "Allow public update" ON trainer_profiles FOR UPDATE TO anon USING (true);
CREATE POLICY "Allow public update" ON student_enrollments FOR UPDATE TO anon USING (true);
CREATE POLICY "Allow public update" ON student_custom_requests FOR UPDATE TO anon USING (true);
CREATE POLICY "Allow public update" ON trainer_classes FOR UPDATE TO anon USING (true);

```
