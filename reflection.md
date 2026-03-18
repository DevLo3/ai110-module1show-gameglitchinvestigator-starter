# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
    At first, the game looked simple and easy to understand. Via the UI I was prompted to guess a number between 1 and 100 and told I had 8 attempts to do so. I could also see there were several buttons I could interact with, such as "Submit Guess", "New Game", and "Show Hint". I could see the game provides the ability to adjust difficulty, which affected the range of valid numbers and the number of available guess attempts. Lastly, I could see a Developer Debug Info section which provided useful insight into the game state and the history it was tracking.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
    Some of the bugs I immediately noticed:
      1. The attempt counter incremented from 0 to 1 upon page refresh, even though no attempt was submitted
        a. I expected my attempt count to remain at 0
      2. The hint text hints in the wrong direction
        a. Based on the debug info, I expected the hints to point in the opposite direction
      3. Entries are not added to history until the Submit button is pressed twice or the hint checkbox is clicked
        a. I expected the submit button to update the history dictionary
      4.  New Game button does not clear history dictionary and also does not properly reset the game, even if you run out of attempts or won during your previous game
        a. I expect the button to reset all game variables and present me with a fresh game 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 
  For this excercise, I used Claude Code as provided to our class by Anthropic.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  One of the bugs I identified when playing the guessing game was the fact that the game did not properly update the history dictionary after a user submitted a guess. Instead, I found I had to press submit twice before my entry was reflected in the debug console. Upon mentioning this to Claude, it was able to identify the issue was due to the debug being rendered before the submit handler activated. Since streamlit process code from top to bottom, this meant that anytime a user would submit a new guess, the debug console was rendered with old information. Claude correctly identified a simple fixed which involved adding a st.rerun() call to the submit handler, which forced the app to re-render the debug console with the newest information anytime a new submission was provided. I was able to verify this by manually testing the functionality myself and then running it through a pytest case.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  One thing I discovered after implementing Claude's suggested fix for the above bug was that the applications hint banner was now broken. It no longer appeared or worked after, even when the "Show hint" checkbox was toggled. It turns out that suggested solution provided by Claude (which I allowed to be implemented) for the above bug inadvertently broke the hint banner functionality by creating log that rendered and wiped a hint in the same interaction before it could ever be displayed to the user. After pointing this out to Claude, we were able to identify a solution to this bug as well.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
