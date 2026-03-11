# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  
  When I first ran the game, it appeared to work on the surface I could enter a number and submit a guess but the hints were always wrong. No matter what number I guessed, the hint kept saying "Go LOWER!" even when my guess was too low, which made the game unwinnable through logic alone.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  1) The hints were backwards. In check_guess, when guess > secret the message said "📈 Go HIGHER!" and when guess < secret it said "📉 Go LOWER!" the exact opposite of what they should say.

  2) Every other guess gave a completely wrong hint due to a type mismatch. On even-numbered attempts, the secret number was secretly converted to a string before being compared. This caused Python to compare numbers as text (e.g., "9" > "42" is True alphabetically), making the hints unreliable even after fixing the first bug.

  3) The New Game button did nothing after a game ended. Clicking it reset the secret and attempt count but never reset st.session_state.status, so the app stayed stuck in "won" or "lost" state and st.stop() blocked everything from loading again.


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude Code as my primary debugging partner throughout this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  When I asked about the hint always saying "Lower," Claude correctly identified that the messages in check_guess were swapped — guess > secret was returning "Go HIGHER!" instead of "Go LOWER!", and vice versa. I verified this by reading lines 37–40 myself and looking into the print statement and confirming the logic: if my guess is too high, I should go lower, not higher. Fixing those two return statements immediately made the hints correct.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
   
 The AI's suggestion for the New Game button bug was initially misleading. It told me to add one missing line of code but didn't specify exactly where to place it, and since there was similar-looking code elsewhere in the file, I added it in the wrong spot. When I told Claude it still wasn't working, it revised its suggestion with more precise details pointing to the exact block and explaining why that specific location mattered. This taught me that when an AI gives a vague fix, it's worth asking for more specifics before making changes.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I decided a bug was fixed by testing the specific scenario that had failed before. For the hint bug, I guessed a number I knew was too high and checked that it now said "Go Lower!" instead of "Go Higher!" For the New Game button, I played until I won or lost, then clicked New Game and verified the game actually reset and let me play again.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  I ran the pytest suite using python3 -m pytest tests/test_game_logic.py -v. The first run showed 3 failures and 4 passes as the 3 original tests were failing because they compared check_guess's return value directly to a string like "Win", but the function actually returns a tuple ("Win", "🎉 Correct!"). This showed me that even tests themselves can have bugs, and that you need to understand what a function actually returns before asserting against it. After fixing the assertions to unpack the tuple (outcome, message = check_guess(...)), all 7 tests passed. The two most useful tests were test_integer_comparison_not_string and test_hint_says_lower_when_guess_too_high, they confirmed that the swapped message bug and the string-comparison bug were both genuinely fixed, not just visually different in the code.

- Did AI help you design or understand any tests? How?
  Yes, I asked Claude to generate pytest cases that specifically targeted the bugs we found. It explained the reasoning behind each test, not just the code. For example, for the string comparison bug, it pointed out that 9 vs 42 is a better test case than something like 30 vs 50, because "9" > "42" as strings but 9 < 42 as integers so that specific pair would catch the bug where a normal pair wouldn't. That helped me understand that good tests aren't just "does it work," they're designed around the exact way something could break. Claude also caught that the original 3 tests had a bug themselves they were asserting against a plain string when the function returned a tuple which showed me that tests need to be read critically, not just trusted.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  In Streamlit, every time you interact with the app clicking a button, typing in a text box and the entire Python script reruns from top to bottom. So if the secret was just written as random.randint(1, 100) at the top of the file with no protection, it would generate a brand new random number on every single interaction, meaning the secret changed every time you submitted a guess. The fix is wrapping it in if "secret" not in st.session_state, which makes Streamlit only generate the number once and store it across reruns. Session state acts like memory that survives each rerun without it, the app has no memory between interactions and everything resets.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine you have a whiteboard where you write your app's instructions. Every time someone clicks a button or types something, someone erases the whole whiteboard and rewrites everything from scratch that's what Streamlit does on every interaction. The problem is, when you erase the board, you also lose any values you calculated, like the random secret number. Session state is like a sticky note on the side of the whiteboard that doesn't get erased you write important values there once, and they survive every rerun. So if "secret" not in st.session_state is basically saying "only write a new secret on the sticky note if there isn't one already" otherwise you'd get a new random number every single time someone clicked anything.

- What change did you make that finally gave the game a stable secret number?
  The secret was already stable thanks to the if "secret" not in st.session_state guard. The real fix was adding st.session_state.status = "playing" to the New Game button and without it, the game stayed locked in a "won" or "lost" state after each round and st.stop() blocked the new secret from ever being played.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I think i would like to resue the testing habits and prompting strategy. 
- What is one thing you would do differently next time you work with AI on a coding task?
  I think from next time instead of asking the solution for the bug i found I would like to ask the AI to give me hints and explain the bug first. Another thing that I'd like to improve is the prompting style. Rather than giving a big chunk of code to the AI i would explain the problem and only provide a certain line of code. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project made me realize that AI-generated code can look completely correct at a glance — proper syntax, sensible variable names, logical structure while hiding subtle bugs that only show up in specific scenarios. I now treat AI-generated code the same way I'd treat code from anyone else: read it critically, test the edge cases, and don't assume it works just because it runs without errors.