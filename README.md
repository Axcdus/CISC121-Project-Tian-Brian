# CISC121-Project-Tian-Brian

# Binary Search Visualisation


## Demo video/gif/screenshot of test
Video: https://youtu.be/WAU5plzJGvM

## Problem Breakdown & Computational Thinking
### Why? 
I chose to create a visual simulation of a binary search algorithm because it used to confuse me, and seeing the steps play out visually always helps me understand how something actually works. Binary search is also easy to visualize since the list is continually cut in half, allowing you to see the search zone shrink clearly. Another reason I chose it is that I will likely be using binary search in a personal project of mine that involves searching for items in a market, so building this simulation helps me learn it properly now before I apply it in that context.

### 4 Pillars of Computational Thinking

#### Decomposition
- Input: User provides a sorted list and a target number

- Validate input (numbers only, sorted, ≤100 elements)

- Initialize search bounds (lower = 0, upper = len(list)-1)

- While lower ≤ upper:

- - Compute mid = (lower + upper) // 2

- - Compare arr[mid] to target

- - Update bounds accordingly

- - Record current step for visualization

- Output: Target index or “not found”

#### Pattern Recognition

- Repeatedly calculate mid

- Compare arr[mid] to target

- Adjust lower or upper depending on comparison

- Stop when target is found or range is exhausted

- Track steps for graph and code highlighting

#### Abstraction
- Show to user:

- - Current search range (lower → upper)

- - mid element being checked

- - Step-by-step movement left/right

- - Found/not found status

- Hide:

- - Internal loop counters, temporary variables

- - Exact memory addresses or unnecessary internal calculations

#### Algorithm Design
- Input → Processing → Output flow:

- - Input: Textbox for sorted list, numeric target

- - Processing: Binary search logic records steps

- - Output:

- - - Graph visualization of array, search range, and mid

- - - Code highlighting current step

- - - Result text (target index or not found)

- - GUI: Buttons for “Start”, “Next Step”, “Previous Step”, “Generate Random List”
 
#### Datatypes & Structures
- Input: String of numbers (comma-separated) → parsed to integer list

- Target: Integer

- Steps stored as list of tuples: (arr, lower, upper, mid, target, found_index)

- Visualization:

- - Graph image (PIL Image)

- - Code step image (PIL Image)

#### Flowchart
<img width="506" height="711" alt="Binary Search Visualization" src="https://github.com/user-attachments/assets/28dcf588-4b45-441f-a451-e65638bdd6df" />


## Steps to Run
1. Enter an ascending order list or use the generate random list button and enter list length (max is 100)
2. Enter any integer as target
3. Click Start Search
4. Use the Next and Previous Step buttons to see how the lower, mid, and upper changes as the search progresses

## Hugging Face Link
https://huggingface.co/spaces/Axcdus/binary-search-visualiser

## Author & Acknowledgment
#### Author
- Brian Tian

- CISC 121 Sec 2

- Professor: Dr. Ruslan

- Project: Binary Search Visualization Tool

#### Acknowledgements
- Dr. Ruslan for teaching binary search
- ChatGPT for help debugging and improving clarity
- HuggingFace Spaces for hosting the interface
