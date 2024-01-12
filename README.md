# Advent of Code 2024 Solutions

Author: Daniel Huang


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Advent of Code 2024 Solutions](#advent-of-code-2024-solutions)
  - [Day 1: Trebuchet](#day-1-trebuchet)
    - [Part 1](#part-1)
    - [Part 2](#part-2)
  - [Day 2: Cube Conundrum](#day-2-cube-conundrum)
    - [Part 1](#part-1-1)
    - [Part 2](#part-2-1)
  - [Day 3: Gear Ratios](#day-3-gear-ratios)
    - [Part 1](#part-1-2)
    - [Part 2](#part-2-2)
  - [Day 4: Scratchcards](#day-4-scratchcards)
    - [Part 1](#part-1-3)
    - [Part 2](#part-2-3)
  - [Day 5: If You Give A Seed A Fertilizer](#day-5-if-you-give-a-seed-a-fertilizer)
    - [Part 1](#part-1-4)
    - [Part 2](#part-2-4)
  - [Day 6: Wait For It](#day-6-wait-for-it)
    - [Part 1](#part-1-5)
    - [Part 2](#part-2-5)
  - [Day 7: Camel Cards](#day-7-camel-cards)
    - [Part 1](#part-1-6)
    - [Part 2](#part-2-6)
  - [Day 8: Haunted Wasteland](#day-8-haunted-wasteland)
    - [Part 1](#part-1-7)
    - [Part 2](#part-2-7)
  - [Day 9: Mirage Maintenance](#day-9-mirage-maintenance)
    - [Part 1](#part-1-8)
    - [Part 2](#part-2-8)
  - [Day 10: Pipe Maze](#day-10-pipe-maze)
    - [Part 1](#part-1-9)
    - [Part 2](#part-2-9)
  - [Day 11: Cosmic Expansion](#day-11-cosmic-expansion)
    - [Part 1](#part-1-10)
    - [Part 2](#part-2-10)
  - [Day 12: Hot Springs](#day-12-hot-springs)
    - [Part 1](#part-1-11)
    - [Part 2](#part-2-11)
  - [Day 13: Point of Incidence](#day-13-point-of-incidence)
    - [Part 1](#part-1-12)
    - [Part 2](#part-2-12)
  - [Day 14: Parabolic Reflector Dish](#day-14-parabolic-reflector-dish)
    - [Part 1](#part-1-13)
    - [Part 2](#part-2-13)
  - [Day 15: Lens Library](#day-15-lens-library)
    - [Part 1](#part-1-14)
    - [Part 2](#part-2-14)
  - [Day 16: The Floor Will Be Lava](#day-16-the-floor-will-be-lava)
    - [Part 1](#part-1-15)
    - [Part 2](#part-2-15)
  - [Day 17: Clumsy Crucible](#day-17-clumsy-crucible)
    - [Part 1](#part-1-16)
    - [Part 2](#part-2-16)
  - [Day 18: Lavaduct Lagoon](#day-18-lavaduct-lagoon)
    - [Part 1](#part-1-17)
    - [Part 2](#part-2-17)
  - [Day 19: Aplenty](#day-19-aplenty)
    - [Part 1](#part-1-18)
    - [Part 2](#part-2-18)
  - [Day 20: Pulse Propagation](#day-20-pulse-propagation)
    - [Part 1](#part-1-19)
    - [Part 2](#part-2-19)
  - [Day 21: Step Counter](#day-21-step-counter)
    - [Part 1](#part-1-20)
    - [Part 2](#part-2-20)
  - [Day 22: Sand Slabs](#day-22-sand-slabs)
    - [Part 1](#part-1-21)
    - [Part 2](#part-2-21)
  - [Day 23: A Long Walk](#day-23-a-long-walk)
    - [Part 1](#part-1-22)
    - [Part 2](#part-2-22)

<!-- /code_chunk_output -->



## Day 1: Trebuchet

### Part 1

<details>
<summary><b>Solution</b></summary>
Since each line is independent of all other lines, a simple loop across all lines is sufficient to solve the problem. For each line, extract all the digits into a list <code>nums: list[int]</code> and query the number as <code>10 * nums[0] + nums[-1]</code>.
</details>

### Part 2

<details>
<summary><b>Solution</b></summary>
Using a similar iteration approach, the algorithm needs to also check for matching words in the future letters. This is then used to build the list of numbers, which is then used to generate the number as before.
</details>

## Day 2: Cube Conundrum

### Part 1

<details>
<summary><b>Solution</b></summary>

This problem is mostly a parsing problem from the text data. This data can be split into hierarchies of functions:

- Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
  - Action: Split by <code>:</code>
  - Game 1
    - Action: Split by <code> </code>
    - Game
    - 1 (Use this as ID)
  - 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    - Action: Split by <code>;</code>
    - 3 blue, 4 red
      - Action: Split by <code>,</code>
      - 3 blue
        - Action: Split by <code> </code>
        - 3 (Use as count)
        - blue (Use as label)
      - 4 red
    - 1 red, 2 green, 6 blue
    - 2 green

After this, an easy comparison between the bag and hand for each grab can be done to determine if the game is valid.
</details>

### Part 2

<details>
<summary><b>Solution</b></summary>
From the previous approach and built data-structure, it is simple to grab the maximum number of dies per color per game, then perform the "sum of power" calculations.
</details>

## Day 3: Gear Ratios

### Part 1

<details>
<summary><b>Solution</b></summary>
Using a grid data structure, iterate through each line and check for each number. Then, grab the neighbors to check for symbols. If there is any, then add to the total.
</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Search instead for <code>*</code> and check for neighboring numbers. If there are exactly two, then multiply them together and add to the total.

**Grid Data Structure**

Grid data structure makes these calculations simple by parsing adjacency lists between each unique number and symbol. This grid is parsed once for the problem, and both parts can then be solved. It maintains an adjacency list of all numbers with ID <code>(x, y, value)</code> and symbols with ID <code>(x, y, symbol)</code> to each other.
</details>

## Day 4: Scratchcards

### Part 1

<details>
<summary><b>Solution</b></summary>
This problem is a parsing problem and a set intersection problem, both of which can easily be done in Python. Simply parse the numbers before and after the <code>|</code> into sets of numbers, and find the intersection using <code>set.intersection</code>.
</details>

### Part 2

<details>
<summary><b>Solution</b></summary>
Using the same parsed cards from part 1, keep track of the number of each card and process them iteratively. Each card just adds to downstream cards, making this a simple iterative problem.
</details>

## Day 5: If You Give A Seed A Fertilizer

### Part 1

<details>
<summary><b>Solution</b></summary>
Parsing the information is relatively simple. To help with calculations, a custom <code>Mapping</code>, <code>Range</code> can be made to keep track of each mapping and range operation. This allows for easy calculation of the resulting location number for every seed through the transformations. Then, the lowest location can be calculated from going through all the seeds.
</details>

### Part 2

<details>
<summary><b>Solution</b></summary>
Enumerating through all the seeds is not feasible due to the large quantity of them. Thus, range operations are required. First, keep track of each seed range. For each mapping, transform them into another set of ranges. The result after applying these transformations is a list of ranges representing the resulting locations. Then, the lowest location can be calculated from the lowest <code>start</code> in each range.
</details>

## Day 6: Wait For It

### Part 1

<details>
<summary><b>Solution</b></summary>

Since the input numbers are relatively small, a simple iteration through the times is sufficient to calculate all the times that will beat the record.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Since the input has now grown extremely large, it becomes infeasible to calculate through iteration. Thus, we need to notice that the problem is equivalent to solving the following quadratic equation:

$$ t (T - t) >= D $$

Where $t$ is the time held, $T$ is the total time, and $D$ is the distance. The two roots are the endpoints of how long we can hold the button. Using the quadratic formula with respect to $t$, we can calculate those two roots, cast them to the appropriate integers using `math.ceil` and `math.floor`, and then subtract them to get the number of ways to win.

</details>

## Day 7: Camel Cards

### Part 1

<details>
<summary><b>Solution</b></summary>

This problem boils down to sorting the card hands into sortable values. To do this, I assigned each card hand with a hex value, where the first digit is the type of hand and the rest of the digits are the card values. Specifically, the cards are ordered as `A: 14`, `K: 13`, `Q: 12`, `J: 11`, `T: 10`, and all digits as their corresponding integer values. Using the rules of poker, it is simple to determine the groupings of each hand by viewing the counts of cards.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Using the same hex value standard but with the Joker as value of `1` (the lowest), the most difficult part of the problem is to determine the largest hand if a hand has jokers. The most simple way to do this is to split the categories into the number of possible values assuming there is at least one Joker.

- Five of a kind must be exactly all Jokers (1 card type) or jokers and one other card (2 card types)
- Four of a kind must have exactly 3 card types and at least one non-joker with only one instance of that card type
- Full house also must have exactly 3 card types and covers all of the other cases that four of a kind does not
- Three of a kind must have exactly 4 card types, one of which is 2 count. If it is the joker, then there is only 1 joker and becomes a 3 of a kind. Otherwise, there are 2 jokers and can be matched with any of the single cards to become a 3 of a kind.
- The only remaining case is 5 card types, which can only produce a single pair or high card. Since we can assume a joker in the hand, there can only be a single pair.

</details>

## Day 8: Haunted Wasteland

### Part 1

<details>
<summary><b>Solution</b></summary>

Using a binary tree, I parsed the data into a set of nodes, each with their left/right children. Then, I simply followed the instructions until reaching `ZZZ` and counted the steps.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Using an iterative approach of part 1 is infeasible due to the large number of steps it would require for all of the paths to converge. From analysis of the given data (though I am not aware of a rigorous proof yet), it is clear that the paths are exactly periodic. Thus, we can calculate the number of steps for each starting position and find the least common multiple of all of them.

</details>

## Day 9: Mirage Maintenance

### Part 1

<details>
<summary><b>Solution</b></summary>

The simplest way to perform this operation is to use a recursive function that predicts the next token by adding the last token with the prediction of the difference sequence as shown in the problem statement. This is also equivalent to performing a polynomial interpolation of the sequence, but due to floating point limitations, it is not accurate enough for this problem set.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Since polynomial extrapolation is equivalent forwards and backward, simply perform the same operation as part 1 but with the sequence reversed.

</details>

## Day 10: Pipe Maze

### Part 1

<details>
<summary><b>Solution</b></summary>

Most of the complexity in this problem is coding in the pipe variations. From this, we can assume that the only pipes connected to the starting position are the ones that are part of the loop. Thus, we can simply perform a BFS from the starting position and find the largest depth from the starting loop.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Using the path obtained from part 1, some logic can be applied to determine whether or not a cell can be part of the nest. Since for each row we start on the "outside" of the loop, we can keep track of a parity variable that flips every time we encounter a non-horizontal pipe ("|", "L", "J", "7", "F"). If we encounter an "L", it can be terminated either by encountering an "J" or "|". Likewise, if we encounter an "F", it can be terminated either by encountering a "7" or "|". Thus, we can keep track of the parity of the row and determine whether or not a cell is part of the nest through row-major iteration.

</details>

## Day 11: Cosmic Expansion

### Part 1

<details>
<summary><b>Solution</b></summary>

The distances is simply the Manhattan distance, which can be calculated using the indices of the galaxies. A simple expansion algorithm can be used to calculate the new indices of the galaxies given a list of empty rows and columns by adding an expansion factor for each row/column before the current index.

An alternate solution of creating a new grid is possible, but it is more memory intensive.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

The solution is exactly the same as Part 1, but with expansion factor of 999999 instead of 1.

</details>

## Day 12: Hot Springs

### Part 1

<details>
<summary><b>Solution</b></summary>

This problem is reminiscent of a single row of a nonogram puzzle. The best method for solving this problem is to brute force all potential configurations of a row given its constraints. This can be done recursively by iterating through all "groups" of `#` and `?` separated by `.`. For each group, we try to put the first assignment of broken springs into the group in as many ways as possible and return the leftover group. Once the broken spring assignments are completed assignment and no more `#` are present in the group, we can confirm that it is indeed a valid assignment.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

The solution to this is equivalent to part 1, just using memoization to avoid recomputing the same configurations.

</details>

## Day 13: Point of Incidence

### Part 1

<details>
<summary><b>Solution</b></summary>

Since there is exactly one reflection, we can iterate through all of the rows and columns to find a valid reflection point. This is feasible due to the small sizes of the arrays using a two-pointer approach.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

This time, we can brute force changing all of the entries since there is exactly one smudge that will change or cause a new reflection. A similar two-pointer approach can be used, just keeping track of all valid positions for the reflection line once the smudge has been tested.

</details>

## Day 14: Parabolic Reflector Dish

### Part 1

<details>
<summary><b>Solution</b></summary>

The tilting logic can be implemented using a column-wise loop around the data. The key is to keep track of an index to place a rock if one is encountered. If a round rock is encountered, place the rock there and increment the index by one. If a cube rock is encountered, move the index to one past the cube rock (since it would block any other round rocks from rolling past it). Calculating the total load can be done through row-wise iteration and multiplying the number of rocks in each row with the multiplier.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Making the cycle logic is just minor tweaks to the `tilt_north` from part 1. However, it is infeasible to loop the `1e9` cycles. The key is to notice that there can be cycles of grid states within the 1e9 cycles. Thus, by keeping track of the grid states and the cycle number, we can calculate the number of cycles to skip and reach the final state. The total load calculation is still equivalent.

</details>

## Day 15: Lens Library

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution is simply to calculate the hash as described in the problem statement.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Simply initialize an array with 256 empty arrays. For each step, parse the token with regex for either adding a lens or removing a lens. Then, grab the hashed value and add/remove the lens from the corresponding box. Finally, calculate the focusing power by iterating through the boxes and multiplying the box number, slot number, and focal length.

</details>

## Day 16: The Floor Will Be Lava

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution is to simulate the beam of light while keeping track of a state to avoid recomputation and loops. To do this, we keep track of `seen` as a set of `pos, direction` encoding the position and direction the beam was going in. Then, we can simulate it using BFS or DFS (tagging the energized cells along the way) until each beam has exited the loop. We can then count the number of energized tiles.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

The solution is to simply brute force all possible starting positions and directions. We can use the same simulation logic as part 1, just iterating through all possible starting positions and directions. Optimizations are possible using caching, but not necessary as the solution runs in around two seconds.

</details>

## Day 17: Clumsy Crucible

### Part 1

<details>
<summary><b>Solution</b></summary>

This can be performed using Dijkstra's algorithm, keeping track of not only seen positions but also the direction and direction counts. This way, the first time a position is seen, it is guaranteed to be the shortest path to that position. The requirement of not moving more than three consecutive blocks can be implemented by keeping track of direction and direction counts and provide only valid directions to move in.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Similar to part 1, the key is to use Dijkstra's algorithm. The only difference is the directions that we provide to the algorithm, which is still dependent on the number of consecutive blocks we have moved in the same direction.

</details>

## Day 18: Lavaduct Lagoon

### Part 1

<details>
<summary><b>Solution</b></summary>

Using the Shoelace method of calculating area and Pick's theorem, we can calculate the number of grid points that are on or inside the polygon outlined by the trench path. The area can be obtained using the vertices through traversing the trench path with the Shoelace method, and the number of interior grid points can be obtained using Pick's theorem. Thus, the number of trench units can be calculated by the sum of boundary and interior points.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

The solution is equivalent to that from part 1. The only difference being that we need to convert the hexadecimal codes into correct instructions, which can be made easy with Python's `int(hex, 16)` function.

</details>

## Day 19: Aplenty

### Part 1

<details>
<summary><b>Solution</b></summary>

After the parsing of the input, we can simulate the workflows through iteratively updating the current workflow and jumping through the rules until it reaches `R` or `A`. Since there are only `>` and `<` rules, the outputs can be written manually with respect to the values and no evaluation needs to be made.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Iterating through all $4000^4$ combinations of ratings is infeasible. Thus, we need to keep track of ranges of ratings. To facilitate this, we can create a `RatingRange` class that keeps track of the minimum and maximum values of each rating. Then, we can iterate through the workflows splitting and updating the ratings while maintaining of queue of ranges and current workflow to process. A process terminates once it reaches `R` or `A`, and the counting is complete once the queue is emptied.

</details>

## Day 20: Pulse Propagation

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution is to simulate the button presses. To keep track of the modules, we can create custom module classes that stores the state/memory of the flip-flops and conjunction modules. Each module implements a `push` function that updates its state and returns the pulses to be sent to the next modules. Then, we can simply just keep a FIFO queue of these modules starting with "button" and push the button 1000 times.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

This problem is particularly intractable if taken in the general case. However, we can observe the module structure and see that they are structured in 4 groups of 12-bit counters. Thus, we can simply count which bits are required for the counters to be activated, and the `rx` module will be pulsed when all counters are pulsed at the same time. That is, we take the LCM of the counters to obtain the number of steps for `rx` to be activated.

</details>

## Day 21: Step Counter

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution to this is simply a BFS from the starting position, keeping track of the number of steps taken. Then, simply count the even steps since 64 is even and all reachable points on the grid walkable within $n$ steps must be of parity $n \mod 2$.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

This solution is intractable with standard BFS. However, we can notice some special features of the input. First, the outer ring, the middle cross going through S, and a diamond are all garden plots. Second, the array is an exact square with the starting position in the center. Lastly, the number of steps is exactly enough for the Elf to walk outside the initial grid and an integer number of plots in addition to that.

From this (and a lot of Reddit research), we can see that the reachable garden plots follows a quadratic form. Thus, we can simply calculate the first three integer plots (65 at 0 extra plots, 196 at 1, and 327 at 2). Then, we can use the quadratic formula to calculate the number of plots at 26501365 steps.

Another method (more clearly derived by [u/YellowZorro](https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/)) derives a method to calculate the number of reachable plots using only the original BFS solution from part 1. The idea is to cache a small amount of searches and extrapolate the solution to a large diamond of searchable areas.

</details>


## Day 22: Sand Slabs

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution is pretty straightforward: simply iterate through the bricks and have them drop as far as they can. Then, create a dictionary of bricks to the bricks that are supporting it. If that contains more than two bricks, it is not safe to disintegrate.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

Using a similar approach to part 1, we simulate disintegrating a brick by removing it from the supports of other bricks. Then, we iterate through all blocks that would fall as a result of that with a queue, tallying up all the bricks that fall. Doing this for all bricks would result in the solution.

Optimizations are possible via caching, but it is not worth it in this case.

</details>

## Day 23: A Long Walk

### Part 1

<details>
<summary><b>Solution</b></summary>

The solution for this is simply a DFS with backtracking, which is relatively simple and fast to implement.

</details>

### Part 2

<details>
<summary><b>Solution</b></summary>

The general solution for this problem is NP-complete, so there is no avoiding brute-forcing the problem. However, the problem space can be reduced significantly if we reduce the time it takes to walk from one junction to another. To do this, we pre-compute a walk through the map from start to end, keeping track of the distances. Then, we can brute force a DFS solution like before.

</details>