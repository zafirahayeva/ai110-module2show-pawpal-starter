# PawPal+ Project Reflection

## 1. System Design
    core actions: create schedule, track tasks, add tasks, enter self & pet info
    classes
        pet - species, name, age 
        task - duration, priority, frequency | tracks status
        owner - pets owned, available slots, preferred times 
        schedule - list of tasks, constraints | generates plan, sorts tasks,

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    I included four classes in my initial UML design: pet, owner, task, and schedule. Pet had species, name, and age attributes. It updated its age and returned its own info. Task had duration,  priority, frequency, and status. It can assign a status and pet. It can reschedule itself and return a summary. Owner had a list of pets, availability, preferred times. It can add and remove pets and update the availability and preferrences. Schedule has the list of tasks, and when it was created and updated. It generates the schedule and can add and remove tasks. It can also sort tasks by priority. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, I added bidirectional mapping to Owner and Task so that tasks are always linked to an owner. This prevents ambiguity about whose schedule a task belongs to.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
    I used AI to implement several methods and to create pytests to validate them. Direct prompts were the most helpful. The prompts were also concise and I made sure to keep my chats separate with a focus on different things. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    When Copilot suggested a simplification for my sorting/filtering algorithm, I opted to not use its suggestion. Adding more features could introduce more bugs. I compared its suggestion with what I currently had and weighed the pros and cons of each. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    I tested sorting, recurrence, conflict detection, filtering, and basic task functions such as adding tasks and updating status. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
    I am decently confident that my schedule works correctly. If I had more time, I would test what happens when an owner does not meet their deadlines, especially if the task is recurring. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am satisified with how the backend logic was implemented. I enjoyed creating the methods for each behavior and then testing them. 
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would focus on implementing more UI features on the actual site. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned how to ask more focused questions and the importance of keeping separate chats. 