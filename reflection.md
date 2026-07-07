# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    My initial UML design focused on creating a clean, hierarchical relationship between the real-world classes.
- What classes did you include, and what responsibilities did you assign to each?
    Owner: Tracks the user's name and holds a dictionary of their pets.
    Pet: Stores pet details and a list of their specific tasks.
    Task: A dataclass holding description, time ("HH:MM"), duration, priority, and frequency.
    Scheduler: A utility class with static methods to sort, filter, and check conflicts across all pets.

**b. Design changes**

- Did your design change during implementation?
    I added 'duration' and 'priority' fields to the 'Task' class during implementation. 
- If yes, describe at least one change and why you made it.
    This was necessary to meet the requirement for a smart daily plan that ranks critical tasks (like medicine) over flexible ones when times overlap.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    The scheduler handles time, duration, and priority levels (1=High, 3=Low). 
- How did you decide which constraints mattered most?
    Time and priority matter most because medical and feeding routines cannot be delayed without impacting a pet's health.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    It only catches exact time collisions (e.g., two tasks at "08:00"). It doesn't track rolling time blocks.
- Why is that tradeoff reasonable for this scenario?
    For a simple daily manager, checking exact slots keeps the logic fast, simple, and easy to test while still catching obvious double-bookings.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI to quickly generate the boilerplate for the Python dataclasses, format the Mermaid.js UML diagram, and write the initial stubs for the pytest suite.
- What kinds of prompts or questions were most helpful?
    The most helpful prompts were highly specific technical requests, such as asking "How do I write a Python lambda function to sort a list of strings formatted as 'HH:MM'?"
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    The AI initially suggested putting all the scheduling logic and data tracking directly inside the Streamlit `app.py` file using nested dictionaries.
- How did you evaluate or verify what the AI suggested?
    I rejected this because I realized this would create messy code so I forced it to keep all logic in `pawpal_system.py` and only using `app.py` for the visual interface.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested the mathematical logic for recurring tasks (adding exactly one day to the due date), list accumulation (ensuring pets actually store added tasks), chronological sorting, and the exact-time conflict detector.
- Why were these tests important?
    These were important because the `Scheduler` is the "brain" of the app; if the backend sorts things incorrectly, the UI is useless.
**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am very confident that the core scheduler works, as verified by a passing pytest suite.
- What edge cases would you test next if you had more time?
    If I had more time, I would test edge cases like invalid user inputs for time (e.g., typing "25:00" or "abc") and test how the recurrence logic handles leap years or rolling over to a new month.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with how the `Scheduler` handles the tie-breaking logic using the `priority` attribute. 
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    If I had another iteration, I would redesign the `detect_conflicts` algorithm to calculate rolling duration windows. Right now, it only flags a conflict if two tasks start at the exact same minute. Upgrading it to recognize that a 45-minute walk starting at "08:00" overlaps with a feeding task at "08:30" would make the scheduling logic much more realistic and robust.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned that when designing systems with AI, the human has to strictly define the edge cases and business rules. The AI can write a standard sorting function in seconds, but as the architect, I had to be the one to decide how priority weights, durations, and time constraints actually interacted to solve the specific problem of managing a pet's daily care.