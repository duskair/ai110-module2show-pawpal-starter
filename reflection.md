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
    
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
