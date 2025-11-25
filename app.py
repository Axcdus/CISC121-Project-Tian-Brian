import gradio as gr
import matplotlib.pyplot as plt
import io
from PIL import Image
from matplotlib.patches import Patch
import random

# ----- Binary Search Logic -----
def binary_search_steps(input_list, target):
    try:
        arr = [int(x.strip()) for x in input_list.split(',')]
        target = int(target)
    except:
        return "Error: Please enter valid numbers (e.g., '1, 3, 5, 7, 9')", []

    if len(arr) > 100:
        return "Error: List cannot have more than 100 elements", []

    if arr != sorted(arr):
        return "Error: List must be sorted", []

    steps = []
    lower, upper = 0, len(arr) - 1
    found_index = -1

    while lower <= upper:
        mid = (lower + upper) // 2
        steps.append((list(arr), lower, upper, mid, target, found_index))
        if arr[mid] == target:
            found_index = mid
            steps.append((list(arr), lower, upper, mid, target, found_index))
            break
        elif arr[mid] < target:
            lower = mid + 1
        else:
            upper = mid - 1

    if found_index == -1:
        steps.append((list(arr), -1, -1, -1, target, -1))

    result_text = f"Target {target} {'found at index ' + str(found_index) if found_index != -1 else 'not found'} in {len(steps)-1} steps."
    return result_text, steps

# ----- Visualization: Graph -----
def create_graph_image(arr, lower, upper, mid, target, found_index):
    plt.switch_backend('Agg')
    fig_width = max(15, len(arr)*0.15)
    fig_height = 6
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    indices = list(range(len(arr)))

    colors = []
    for i in range(len(arr)):
        if found_index != -1 and i == found_index:
            colors.append('green')
        elif lower <= i <= upper and found_index == -1:
            if i == mid:
                colors.append('red')
            elif i == lower:
                colors.append('orange')
            elif i == upper:
                colors.append('purple')
            else:
                colors.append('lightcoral')
        else:
            colors.append('lightblue')

    bars = ax.bar(indices, arr, color=colors, alpha=0.8, edgecolor='black')

    if len(arr) <= 50:
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2, str(arr[i]), ha='center', va='bottom', fontsize=8)
            ax.text(bar.get_x() + bar.get_width()/2., -0.5, f'[{i}]', ha='center', va='top', fontsize=8)

    if found_index != -1:
        step_text = f"Target {target} found at index {found_index}."
    elif mid != -1:
        mid_val = arr[mid]
        if mid_val < target:
            step_text = f"Checking index {mid} (value {mid_val}) → move right. Range: [{lower},{upper}]"
        elif mid_val > target:
            step_text = f"Checking index {mid} (value {mid_val}) → move left. Range: [{lower},{upper}]"
        else:
            step_text = f"Target {target} found at index {mid}."
    else:
        step_text = "Target not found."

    ax.set_title("Binary Search Step Visualization", fontsize=14)
    ax.text(0, max(arr)*1.05, step_text, fontsize=12, color='blue', fontweight='bold')

    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_xticks(indices if len(arr) <= 50 else [])

    legend_elements = [
        Patch(facecolor='lightblue', label='Not in search range'),
        Patch(facecolor='lightcoral', label='Middle of current search range'),
        Patch(facecolor='orange', label='First element of current search range'),
        Patch(facecolor='purple', label='Last element of current search range'),
        Patch(facecolor='red', label='Mid element'),
        Patch(facecolor='green', label='Found target')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ----- Visualization: Code Step -----
def create_code_step_image(arr, lower, upper, mid, target, found_index):
    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(6,4))
    ax.axis('off')

    code_lines = [
        "1. mid = (lower + upper) // 2",
        "2. if arr[mid] == target:",
        "3.     return mid",
        "4. elif arr[mid] < target:",
        "5.     lower = mid + 1",
        "6. else:",
        "7.     upper = mid - 1"
    ]

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

    for i, line in enumerate(code_lines):
        color = "red" if i == highlight_line else "black"
        ax.text(0.01, 0.9 - i*0.12, line, fontsize=12, color=color, fontweight='bold' if i == highlight_line else 'normal', va='top', ha='left')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ----- Random List Generator -----
def generate_random_list(length):
    length = max(1, min(length, 100))  # Clamp between 1 and 100
    arr = sorted(random.sample(range(1, length*3), length))
    arr_str = ",".join(map(str, arr))
    return arr_str

# ----- Step Controller -----
class StepController:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.result_text = ""

    def start(self, input_list, target):
        self.result_text, self.steps = binary_search_steps(input_list, target)
        self.current_step = 0
        if self.steps:
            return (self.result_text,
                    create_graph_image(*self.steps[0]),
                    create_code_step_image(*self.steps[0]))
        else:
            return self.result_text, None, None

    def next_step(self):
        if self.steps:
            self.current_step = min(self.current_step + 1, len(self.steps)-1)
            return (self.result_text,
                    create_graph_image(*self.steps[self.current_step]),
                    create_code_step_image(*self.steps[self.current_step]))
        return self.result_text, None, None

    def prev_step(self):
        if self.steps:
            self.current_step = max(self.current_step - 1, 0)
            return (self.result_text,
                    create_graph_image(*self.steps[self.current_step]),
                    create_code_step_image(*self.steps[self.current_step]))
        return self.result_text, None, None

controller = StepController()

# ----- Gradio Interface -----
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

    gen_random_btn.click(generate_random_list, inputs=[random_len], outputs=[input_list])
    start_btn.click(controller.start, inputs=[input_list, target], outputs=[result_text, graph_img, code_img])
    prev_btn.click(controller.prev_step, inputs=[], outputs=[result_text, graph_img, code_img])
    next_btn.click(controller.next_step, inputs=[], outputs=[result_text, graph_img, code_img])

if __name__ == "__main__":
    demo.launch()
