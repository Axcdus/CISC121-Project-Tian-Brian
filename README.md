# CISC121-Project-Tian-Brian

# Binary Search Visualisation


## Demo video/gif/screenshot of test


## Problem Breakdown & Computational Thinking (You can add a flowchart and write the four pillars of computational thinking briefly in bullets)
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

#### Algorithm Design


## Steps to Run


## Hugging Face Link


## Author & Acknowledgment
