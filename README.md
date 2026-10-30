# WaveFlow: Wave Start Scheduler and Runner Tracker

**Group 1** | Operating System (BNF32303) POPBL | Theme: Wave Starts & Runner Tracking

## Team members
| Name | Matric no. |
|---|---|
| EMIR SULAIMAN BIN KHAIRUL FAIZI | AN260074 |
| AMIR WAFIQ BIN MOHD ROSLAN | CN260417 |
| MUHAMMAD AMMAR BIN SUANDI HALIL | CN260249 |
| HARIS SHARAFUDDIN BIN ANUAR | CN260379 |
| MOHAMMAD ASYRAF KHUZAIRIE BIN HAMZANI | CN260297 |

## Theme and OS concepts
A community fun run releases runners in waves, but only one wave can use the start line at a time. WaveFlow treats each wave as a process and the start line as the CPU. It implements FCFS, Round Robin and Priority scheduling, tracks every wave through the states New, Ready, Running, Blocked and Terminated, and compares the algorithms by average waiting, turnaround and response time.

## Install and run
```bash
git clone <repo-url>
cd OS-POPBL-Group1-RunnerTracking
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

Run the tests with `python -m pytest`.

## Folders
- `src/` source code
- `docs/` proposal, architecture diagram, technical report
- `assets/` posters, slides, screenshots
- `tests/` unit tests

Run the tests with `python -m pytest`.



