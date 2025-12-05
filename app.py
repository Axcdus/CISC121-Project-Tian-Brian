import gradio as gr
import matplotlib.pyplot as plt
import io
from PIL import Image
from matplotlib.patches import Patch
import random

# ============================================================
#                    BINARY SEARCH LOGIC
# ============================================================
def binary_search_steps(input_list, target):
    """
    Parses the input list, validates it, and performs
    binary search while saving each step for visualization.
    """
    # --- Parse input safely ---
    try:
        arr = [int(x.strip()) for x in input_list.split(',')]
        target = int(target)
    except:
        return "Error: Please enter valid numbers (e.g., '1, 3, 5, 7, 9')", []

    # --- Enforce maximum list size ---
    if len(arr) > 100:
        return "Error: List cannot have more than 100 elements", []

    # --- List must be sorted for binary search ---
    if arr != sorted(arr):
        return "Error: List must be sorted", []

    # --- Prepare variables for binary search ---
    steps = []              # Stores snapshots for visualization
    lower, upper = 0, len(arr) - 1
    found_index = -1

    # ============================================================
    #                 BINARY SEARCH PROCESS
    # ============================================================
    while lower <= upper:
        mid = (lower + upper) // 2

        # Save the current snapshot before deciding next step
        steps.append((list(arr), lower, upper, mid, target, found_index))

        # --- Case 1: target found ---
        if arr[mid] == target:
            found_index = mid
            # Save final "found" step
            steps.append((list(arr), lower, upper, mid, target, found_index))
            break

        # --- Case 2: target is larger → search right half ---
        elif arr[mid] < target:
            lower = mid + 1

        # --- Case 3: target is smaller → search left half ---
        else:
            upper = mid - 1

    # If not found, append a final step showing that
    if found_index == -1:
        steps.append((list(arr), -1, -1, -1, target, -1))

    # --- Create result message ---
    result_text = (
        f"Target {target} "
        f"{'found at index ' + str(found_index) if found_index != -1 else 'not found'} "
        f"in {len(steps)-1} steps."
    )
    return result_text, steps

# ============================================================
#               GRAPH VISUALIZATION FOR EACH STEP
# ============================================================
def create_graph_image(arr, lower, upper, mid, target, found_index):
    """
    Draws a bar graph showing the current binary search state:
    - which indices are in range
    - the mid index
    - where the target is found
    """
    plt.switch_backend('Agg')

    # --- Scale graph width based on list size ---
    fig_width = max(15, len(arr) * 0.15)
    fig_height = 6
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    indices = list(range(len(arr)))

    # --- Determine bar colors ---
    colors = []
    for i in range(len(arr)):
        if found_index != -1 and i == found_index:
            colors.append('green')  # Found target
        elif lower <= i <= upper and found_index == -1:
            if i == mid: colors.append('red')         # Mid element
            elif i == lower: colors.append('orange')  # Range start
            elif i == upper: colors.append('purple')  # Range end
            else: colors.append('lightcoral')         # In search range
        else:
            colors.append('lightblue')                # Outside range

    bars = ax.bar(indices, arr, color=colors, alpha=0.8, edgecolor='black')

    # --- Show numbers only for small lists ---
    if len(arr) <= 50:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    str(arr[i]), ha='center', fontsize=8)
            ax.text(bar.get_x() + bar.get_width()/2., -0.5,
                    f'[{i}]', ha='center', fontsize=8)

    # --- Step explanation text ---
    if found_index != -1:
        step_text = f"Target {target} found at index {found_index}."
    elif mid != -1:
        mid_val = arr[mid]
        if mid_val < target:
            step_text = f"Checking index {mid} (value {mid_val}) → move right."
        elif mid_val > target:
            step_text = f"Checking index {mid} (value {mid_val}) → move left."
        else:
            step_text = f"Target {target} found at index {mid}."
    else:
        step_text = "Target not found."

    ax.set_title("Binary Search Step Visualization", fontsize=14)
    ax.text(0, max(arr)*1.05, step_text, fontsize=12, color='blue')

    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_xticks(indices if len(arr) <= 50 else [])

    # --- Legend ---
    legend_elements = [
        Patch(facecolor='lightblue', label='Not in search range'),
        Patch(facecolor='lightcoral', label='In search range'),
        Patch(facecolor='orange', label='Start of range'),
        Patch(facecolor='purple', label='End of range'),
        Patch(facecolor='red', label='Mid element'),
        Patch(facecolor='green', label='Found target')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # --- Convert plot to image ---
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ============================================================
#            CODE HIGHLIGHT VISUALIZATION (SIMULATED)
# ============================================================
def create_code_step_image(arr, lower, upper, mid, target, found_index):
    """
    Highlights the relevant line of pseudocode based on
    the current state of the binary search.
    """
    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off')

    # Pseudocode displayed
    code_lines = [
        "1. mid = (lower + upper) // 2",
        "2. if arr[mid] == target:",
        "3.     return mid",
        "4. elif arr[mid] < target:",
        "5.     lower = mid + 1",
        "6. else:",
        "7.     upper = mid - 1"
    ]

    # Determine which line to highlight
    if found_index != -1:
        highlight_line = 2
    elif mid != -1:
        if arr[mid] == target:
            highlight_line = 2
        elif arr[mid] < target:
            highlight_line = 4
        else:
            highlight_line = 6
    else:
        highlight_line = -1

    # Draw pseudocode lines
    for i, line in enumerate(code_lines):
        color = "red" if i == highlight_line else "black"
        ax.text(0.01, 0.9 - i*0.12, line,
                fontsize=12, color=color,
                fontweight=('bold' if i == highlight_line else 'normal'))

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ============================================================
#                 RANDOM SORTED LIST GENERATOR
# ============================================================
def generate_random_list(length):
    """
    Generates a sorted random list of up to 100 integers.
    """
    length = max(1, min(length, 100))  # Clamp input
    arr = sorted(random.sample(range(1, length * 3), length))
    return ",".join(map(str, arr))

# ============================================================
#                STEP CONTROLLER FOR NAVIGATION
# ============================================================
class StepController:
    """
    Stores all search steps and allows moving forward/backward.
    """
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.result_text = ""

    def start(self, input_list, target):
        # Initialize binary search and load steps
        self.result_text, self.steps = binary_search_steps(input_list, target)
        self.current_step = 0

        if self.steps:
            return (
                self.result_text,
                create_graph_image(*self.steps[0]),
                create_code_step_image(*self.steps[0])
            )
        return self.result_text, None, None

    def next_step(self):
        # Move forward but not past final step
        if self.steps:
            self.current_step = min(self.current_step + 1, len(self.steps) - 1)
            return (
                self.result_text,
                create_graph_image(*self.steps[self.current_step]),
                create_code_step_image(*self.steps[self.current_step])
            )
        return self.result_text, None, None

    def prev_step(self):
        # Move backward but not before step 0
        if self.steps:
            self.current_step = max(self.current_step - 1, 0)
            return (
                self.result_text,
                create_graph_image(*self.steps[self.current_step]),
                create_code_step_image(*self.steps[self.current_step])
            )
        return self.result_text, None, None


controller = StepController()

# ============================================================
#                         GRADIO UI
# ============================================================
with gr.Blocks() as demo:
    gr.Markdown("# 🔍 Binary Search Visualizer (Step-by-Step)")

    with gr.Row():
        with gr.Column():
            input_list = gr.Textbox(label="Sorted numbers", value="1,3,5,7,9,11,13")
            target = gr.Number(label="Target", value=7)
            random_len = gr.Number(label="Random list length (max 100)", value=10)

            gen_random_btn = gr.Button("Generate Random List")
            start_btn = gr.Button("Start Search", variant="primary")
            prev_btn = gr.Button("Previous Step")
            next_btn = gr.Button("Next Step")

        with gr.Column():
            result_text = gr.Textbox(label="Result")
            graph_img = gr.Image(label="Graph Visualization")
            code_img = gr.Image(label="Code Step Highlight")

    # Button wiring
    gen_random_btn.click(generate_random_list, inputs=[random_len], outputs=[input_list])
    start_btn.click(controller.start, inputs=[input_list, target], outputs=[result_text, graph_img, code_img])
    prev_btn.click(controller.prev_step, outputs=[result_text, graph_img, code_img])
    next_btn.click(controller.next_step, outputs=[result_text, graph_img, code_img])

# Launch application
if __name__ == "__main__":
    demo.launch()
