<a id="top"></a>
<div align="center">

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/banner.svg" alt="Campus Connect: run every student club on campus from one place" width="100%">

<br>
<br>

Campus admins approve clubs and set the rules. Club leaders run members, events and announcements.<br>
Students discover clubs, register for events and collect certificates anyone can verify.

<br>

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue_3-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_AI-D97757?style=for-the-badge&logo=anthropic&logoColor=white)

</div>

<br>

<a id="features"></a>

## Features

<table>
<tr>
<td width="33%" valign="top">

#### Campus Admin
- Approve or reject club proposals
- Publish club guidelines and the application template
- Watch the college leaderboard

</td>
<td width="33%" valign="top">

#### Club Leader
- Run a club dashboard with quick actions
- Approve join requests and manage the roster
- Create events, mark attendance, declare results
- Post announcements and answer member issues

</td>
<td width="33%" valign="top">

#### Student
- Find clubs, or ask the **AI Club Finder**
- Register for events across all your clubs
- Earn **QR-verifiable PDF certificates**
- Raise issues and follow the leaderboard

</td>
</tr>
</table>

<br>

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/event-flow.svg" alt="Event lifecycle: Draft, Published, Registration, Attendance, Results, Certificate, public verify page. A published event can also be cancelled." width="100%">

Every certificate records one of three results, **Winner**, **Runner-up** or **Participant**, and its QR code links to a public verification page.

<br>

<a id="tour"></a>

## Product tour

Each tour plays through that role's screens on its own. Expand a role to watch it, and use the links under it to open any screen at full resolution.

<details open>
<summary><b>Campus Admin</b> &nbsp;·&nbsp; approve clubs and set the rules</summary>
<br>

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/tour-admin.gif" alt="Campus Admin tour: Club Approvals and Club Guidelines" width="100%">

<sub>Full size: [Club Approvals](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/admin-approvals.png) · [Club Guidelines](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/admin-guidelines.png)</sub>

</details>

<details>
<summary><b>Club Leader</b> &nbsp;·&nbsp; run the club day to day</summary>
<br>

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/tour-leader.gif" alt="Club Leader tour: My Club, Members, Events and Issues" width="100%">

<sub>Full size: [My Club](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/leader-my-club.png) · [Members](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/leader-members.png) · [Events](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/leader-events.png) · [Issues](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/leader-issues.png)</sub>

</details>

<details>
<summary><b>Student</b> &nbsp;·&nbsp; discover, take part, get recognised</summary>
<br>

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/tour-student.gif" alt="Student tour: Events, Announcements, Leaderboard, Propose a Club and Help & Issues" width="100%">

<sub>Full size: [Events](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-events.png) · [Announcements](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-announcements.png) · [Leaderboard](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-leaderboard.png) · [Propose a Club](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-propose-club.png) · [Help & Issues](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-issues.png)</sub>

</details>

<details>
<summary><b>Certificates</b> &nbsp;·&nbsp; earned, downloadable and verifiable</summary>
<br>

<img src="https://raw.githubusercontent.com/Srivastava-Shrestha/Assets/main/CampusConnect/tour-certs.gif" alt="Certificates tour: profile with certificates and the certificate PDF" width="100%">

<sub>Full size: [My Profile](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/student-profile.png) · [Certificate PDF](https://github.com/Srivastava-Shrestha/Assets/blob/main/CampusConnect/screens/certificate.png)</sub>

</details>

<br>

<a id="built-with"></a>

## Built with

<table>
<tr>
<td width="50%" valign="top">

#### Backend

| Tool | Purpose |
|---|---|
| **FastAPI** | Async web framework for the REST API |
| **SQLAlchemy 2** | Async ORM for all models and queries |
| **PostgreSQL** | The application database |
| **asyncpg** | High-performance async Postgres driver |
| **Alembic** | Schema migrations |
| **python-jose** | Signs and verifies JWT access tokens |
| **bcrypt** | Hashes user passwords |
| **google-auth** | Verifies Google Sign-In tokens |
| **boto3** | Uploads certificate PDFs to AWS S3 |
| **CairoSVG** | Renders certificate templates into PDFs |
| **qrcode** | Generates the verification QR on each certificate |
| **Jinja2** | Templates certificates and outbound emails |
| **Anthropic** | Powers the AI club-finder assistant |
| **Uvicorn** | ASGI server that runs the app |

</td>
<td width="50%" valign="top">

#### Frontend

| Tool | Purpose |
|---|---|
| **VueJS 3** | Dynamic, reactive user interfaces |
| **Vue Router 4** | Client-side routing and route guards |
| **Pinia** | Application state |
| **Vite** | Fast development environment |
| **Lucide Icons** | A wide set of customizable icons |
| **jwt-decode** | Reads role and college from the access token |
| **CSS** | One central design-system stylesheet |
| **Vitest** | Unit and component tests with Vue Test Utils |

</td>
</tr>
</table>

<br>

<a id="installation"></a>

## Installation

> **Prerequisites:** Python 3.12+ (managed by uv), Node 20+, npm 10+ and PostgreSQL.

<details open>
<summary><b>Backend setup</b></summary>

#### 1. Clone the repository
```bash
git clone https://github.com/Srivastava-Shrestha/MAY2026-Team-003.git
cd MAY2026-Team-003
```

#### 2. Install uv
The backend uses [uv](https://docs.astral.sh/uv/) to manage Python 3.12+ and its dependencies.

Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 3. Install backend dependencies
```bash
cd backend
uv sync
```

#### 4. Configure the backend environment
```bash
cp .env.example .env
```
Then fill in the values. `DATABASE_URL` must use the `postgresql+asyncpg://` scheme. You can generate `JWT_SECRET_KEY` with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

> [!WARNING]
> Point `TEST_DATABASE_URL` at a throwaway database. The test suite drops every table on teardown, so it must never share a database with `DATABASE_URL`.

#### 5. Create the database schema
```bash
uv run alembic upgrade head
```

#### 6. Run the backend
```bash
uv run uvicorn main:app --reload
```
The API runs at `http://localhost:8000`, with Swagger UI at `/docs` and ReDoc at `/redoc`.

</details>

<details open>
<summary><b>Frontend setup</b></summary>

#### 7. Install frontend dependencies
In a new terminal:
```bash
cd ../frontend
npm install
```

#### 8. Configure the frontend environment
Create a `.env` file in the `frontend` directory:
```bash
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-google-oauth-client-id
```

> [!NOTE]
> `VITE_GOOGLE_CLIENT_ID` is the OAuth client ID for the Google Sign-In button. It must match `GOOGLE_CLIENT_ID` in the backend `.env`. Leave it blank to run without Google Sign-In.

#### 9. Run the development server
```bash
npm run dev
```
The app runs at `http://localhost:5173`.

</details>

**You're all set.** Sign in with one of the demo accounts below.

<br>

<a id="demo-credentials"></a>

## Demo credentials

Every demo account uses the password **`12345678`**.

| Role | Email | What it demonstrates |
|---|---|---|
| **Campus Admin** | `shrestha@ds.study.iitm.ac.in` | Club approval queue, all clubs by status, college leaderboard |
| **Club Leader** | `aarav.menon@ds.study.iitm.ac.in` | Leads CodeCrafters with 5 members. Creates and publishes events, marks attendance, declares results, answers issues, posts announcements |
| **Member with certificates** | `sara.khan@ds.study.iitm.ac.in` | Holds 3 certificates covering WINNER, RUNNER_UP and PARTICIPANT, plus notifications and event registrations |

<details>
<summary>More demo students</summary>
<br>

All on `@ds.study.iitm.ac.in`: `diya.sharma`, `kabir.rao`, `ananya.iyer`, `meera.nair`, `rohan.gupta`, `ishita.bose`, `vikram.reddy`, `aditya.verma`, `nikita.joshi`, `arjun.pillai`.

</details>

<br>

## Demo data

The demo runs on one complete college, **IIT Madras BS Degree**, on the domain `ds.study.iitm.ac.in`. Club names, descriptions, logos and social links come from the real IITM BS societies.

<details>
<summary><b>See what's seeded</b></summary>
<br>

**Clubs (7)** cover all four statuses, so every admin view has content:

| Status | Clubs |
|---|---|
| `ACTIVE` | CodeCrafters (Technology), IRIS (Arts & Media), AKORD (Music), RAAHAT (Health & Wellness) |
| `PENDING` | Women in Tech, waiting in the admin approval queue |
| `REJECTED` | Heighers eSports, the one UNOFFICIAL club |
| `ARCHIVED` | Deva-Bhasha Sanskrit Society |

**Events (9):** 4 completed with attendance marked and results declared, 3 upcoming and open for registration, 1 draft and 1 cancelled. One event has no capacity limit.

**Certificates (15):** real PDFs from the app's own renderer, each with a QR code that resolves to `/verify/<serial>`. 13 are stored on S3 and 2 use the Postgres fallback, so both storage paths can be shown.

**Also seeded:** 23 memberships across approved, pending and rejected states. 7 announcements across all 5 categories, 2 of them pinned. 6 issues covering all 5 categories and all 3 statuses. 10 notifications across all 5 types. A leaderboard that ranks the 4 active clubs on real activity scores.

Every column of every table is populated, and every enum value appears at least once.

</details>

<br>

<a id="team"></a>

## Team

**Team 003 (Nexmind)**, BSCS3001 Software Engineering Project, May 2026.

| Member | Role | Commits | PRs (merged) | Branches |
|---|---|:---:|:---:|:---:|
| **Shrestha** | Backend and System Architect | 248 | 32 (27) | 21 |
| **Shrishti** | Frontend | 10 | 12 (10) | 10 |
| **Atharv** | Product Manager | 71 | 13 (13) | 7 |
| **Pawan** | Testing | 46 | 14 (13) | 13 |
| **Kavisha** | Scrum Master | 4 | 0 | 0 |
| `github-actions[bot]` | CI automation | 92 | 0 | 0 |
| | **Total** | **471** | **71 (63)** | **51** |

<br>

## Documentation

| Where | What |
|---|---|
| [`backend/README.md`](backend/README.md) | Backend setup, configuration and testing |
| [`frontend/README.md`](frontend/README.md) | Frontend setup, structure and design system |
| [`backend/openapi.yaml`](backend/openapi.yaml) | Full API spec with endpoints, user story mapping, role matrix and error catalogue |
| [`RULES.md`](RULES.md) | Team working agreement |

<hr>

<div align="center">

### Thank you 🐻

<sub>Made by Team Nexmind</sub>

<br>

[Back to top](#top)

</div>
