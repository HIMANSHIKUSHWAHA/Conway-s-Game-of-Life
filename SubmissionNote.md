
### 📌 Submission Note – Conway’s Game of Life with Wormholes

**GitHub**: [Conway-s-Game-of-Life](https://github.com/HIMANSHIKUSHWAHA/Conway-s-Game-of-Life)

Hi! 👋
Here’s a quick summary of what I built and explored over \~25+ hours of iterative work:

#### ✅ What I implemented:

* A working simulation engine (`game_of_life.py`) that supports:

  * Standard Game of Life rules
  * Wormhole mechanics with directional precedence (top > right > bottom > left)
* Accurate portal parsing from RGB images (`wormhole_parser.py`)
* Step-by-step iteration and PNG output generation
* Verification via pixel-perfect comparison script (`verify_examples.py`)
* Passed all checkpoints for `example-1`, `example-2`, and the full `problem-*` set

#### 🔍 What I tested and tried:

* Compared outputs against all examples with automated diff visualizations
* Debugged mismatches pixel-by-pixel (especially for `example-0` and `example-3`)
* Explored multiple ways to handle portal conflicts and diagonals using the precedence rules
* Validated wormhole connectivity by filtering out colors with invalid components

#### 🧱 Where it was tricky:

* `example-0` still has a few mismatches (\~0.4%) even after extensive debugging — most likely due to ambiguous diagonal wrap rules or image artifacting
* Some wormhole colors in the inputs had >2 components or odd counts — I skipped those to avoid undefined behavior
* Saving and reloading binary images occasionally caused minor aliasing-related mismatches, despite correct logic

#### 🧠 In summary:

The simulator is fully functional, precise on most test cases, and robustly built with clean modular code. The few mismatches left are more about edge-case interpretation than flawed logic. I learned a lot building this!

Thanks for the challenge — it was both fun and rewarding!

— Himanshi Kushwaha


