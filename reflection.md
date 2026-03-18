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
    I decided a bug was truly fixed by manually running through the part of the app where its functionality existed. In doing this, I interacted with it as a user would and ensured the app's logic provided the expected outcome(s).
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    One simple test I ran involved just submitting random numbers to the game with the "Show hint" check box toggled on and ensuring the hint displayed was directionally accurated based on what I knew the number to be
- Did AI help you design or understand any tests? How?
    Absolutely. AI helped design the pytest cases, and answered all questions I had to further my understand of the game's logic and the streamlit platform and its capabilities.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
    From my observation, the secret number didn't actually change between guesses, it was always stored correctly in `st.session_state`. What made the game feel broken was that on even-numbered attempts, the code was secretly converting the secret number from an integer to a string before comparing it to the player's guess. This caused the comparison logic to behave differently depending on the attempt number, making correct guesses register as wrong and the hints point in misleading directions. It looked like the secret was changing, but really the type of the value being compared was changing underneath.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
    I'd explain it this way: every time you interact with a Streamlit app (clicking a button, checking a box, typing in a field) the entire Python script runs again from top to bottom, like hitting refresh on the logic. That means any regular Python variable you create gets wiped and recreated every single time. Session state is Streamlit's solution to this: it's a special dictionary that persists across those reruns, so values you store there survive the script restarting. The catch is you have to be deliberate about what you put in it and when, because the order in which things render and the order in which state changes are applied can cause subtle bugs. We ran into this a couple of times throughout this project.
- What change did you make that finally gave the game a stable secret number?
    The secret was already being stored in `st.session_state`, so the real fix was understanding the `if "secret" not in st.session_state` guard clause. This pattern ensures the secret is only randomly generated once — on the very first page load — and skipped on every subsequent rerun. Once I understood that this guard is what protects all persistent state in Streamlit, the rest of the state bugs became much easier to reason about and fix.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    One habit I want to carry forward is using AI to identify the root cause and location of a bug before attempting a fix. On several occasions in this project I described what I was observing and asked Claude where in the code that behavior was coming from, rather than jumping straight to asking for a solution. This made it easier to understand the fix when it came and also helped me catch cases where Claude's suggested fix introduced a new problem, because I understood the underlying logic well enough to notice something was off.
- What is one thing you would do differently next time you work with AI on a coding task?
    Next time I would test each AI-suggested fix more thoroughly before moving on. There were a couple of moments in this project where I accepted a fix, it resolved the immediate issue, but it silently broke something else that I only caught later. Building a habit of running the full test suite and manually walking through the affected flow after every change — not just verifying the specific bug — would have caught those regressions earlier and saved time.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
    Before this project I think I treated AI-generated code as either correct or obviously wrong, but this project showed me it occupies a messier middle ground. It can be locally correct while being globally broken, fixing one thing while quietly introducing another. I now think of AI as a capable but fallible collaborator that still needs a human in the loop who understands the codebase well enough to catch what the AI misses.
    
