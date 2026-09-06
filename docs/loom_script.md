# Loom Video Script (2:40–3:00 total)

Speak naturally — this is a guide, not a word-for-word script to read robotically. Pause between sections to switch screens.

---

**0:00–0:20 — Introduction**

> "Hi, I'm [Your Name], and this is my QA testing assignment for the OrangeHRM Open Source Demo application. In this walkthrough, I'll cover the manual test cases I wrote, a few potential issues I found on the login page, and then I'll demo the Selenium automation framework I built using the Page Object Model."

---

**0:20–0:50 — Manual test cases**

*(Screen: open `docs/manual_test_cases_login.md` and `docs/manual_test_cases_employee_management.md`)*

> "For manual testing, I wrote 15 test cases for the login page, covering positive scenarios like valid login, negative scenarios like invalid credentials, boundary cases like empty fields, and a few usability checks — for example, whether the username field is case-sensitive, and whether leading or trailing spaces are trimmed. I actually executed these against the live demo site rather than guessing the results, so the Actual Result column reflects real, observed behavior. For anything I couldn't safely test — like repeated failed login attempts, since this is a shared public demo used by many people — I marked it 'To be verified' instead of making something up.
>
> I also wrote 13 test cases for the Employee Management module — adding, listing, updating, and deleting employees — following the same approach."

---

**0:50–1:20 — Bug identification**

*(Screen: open `docs/bug_reports.md`)*

> "For the bug-reporting part, I identified three potential issues on the login page. The first is that the username field doesn't trim leading or trailing whitespace, so a stray space causes a login failure with no specific explanation. The second is that the app shows the same generic 'Invalid credentials' message regardless of whether the username or the password was wrong — which is actually good security practice, so I documented that as an intentional usability trade-off rather than a bug. The third is that I couldn't verify whether there's any brute-force protection, like account lockout, after repeated failed attempts — I intentionally didn't test that against the shared public demo, since it could lock out other people using it at the same time. I labeled each of these clearly as a 'Potential Bug' or a documented usability observation, not a confirmed defect, since I don't have access to the actual requirements or security design."

---

**1:20–2:20 — Automation framework and demo**

*(Screen: open the project folder structure, then run the tests)*

> "For automation, I built a Python Selenium framework using the Page Object Model. The project is organized into a `pages` folder with one class per page — Login, Dashboard, PIM, and Employee — a `tests` folder with the actual test logic and assertions, and a `utils/config.py` file with shared settings like URLs and timeouts. I used explicit waits everywhere instead of hard-coded sleeps, and Selenium's WebDriverManager so the ChromeDriver installs automatically.
>
> The main automated workflow logs in using the credentials shown on the page itself, navigates to PIM, adds four employees with unique names, then goes to the Employee List and searches for each one to confirm it was created — printing 'Name Verified' for each match — and finally logs out and confirms we're back on the login page.
>
> One real thing I ran into while building this: the demo is a shared public instance, so the auto-suggested Employee ID sometimes collides with a record someone else just created. I handled that by detecting the 'Employee Id already exists' error and retrying with a new ID automatically, instead of just letting the test fail on something unrelated to the feature being tested."

*(Show the terminal running `pytest tests/test_employee_management.py -v` and let the "Created employee ID..." and "Name Verified" lines print)*

---

**2:20–2:40 — Test execution/results**

*(Screen: terminal showing the full pytest run)*

> "Here's the full suite running — 11 login tests and the employee management workflow, all passing. If a test fails, the framework automatically saves a screenshot into the `screenshots` folder so I can see exactly what the page looked like at the moment of failure, which made debugging a lot faster while I was building this."

---

**2:40–3:00 — GitHub repository and conclusion**

*(Screen: GitHub repository page)*

> "The full project — source code, test cases, and documentation — is pushed to GitHub at [read out your repo URL]. That wraps up my assignment: manual test cases with real, verified results, honestly-labeled potential bugs, and a working Selenium automation framework with the Page Object Model. Thanks for watching."
