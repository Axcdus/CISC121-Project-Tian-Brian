import gradio as gr

def binary_search_visualize(input_list, target):
    # Convert string input to list of integers
    try:
        arr = [int(x.strip()) for x in input_list.split(',')]
        target = int(target)
    except:
        return "Error: Please enter valid numbers (e.g., '1, 3, 5, 7, 9')"

  # Binary Search process
  steps = []
  lower, upper = 0, len(arr) - 1
  while lower <= upper:
    mid = (lower + upper) // 2
    steps.append({
            'lower': lower, 
            'upper': upper, 
            'mid': mid,
            'mid_value': arr[mid]
        })
    if arr[mid] == target:
      return mid, steps
    elif arr[mid] < target:
      lower = mid+1
    else:
      upper = mid-1
  return -1, steps

# Gradio interface
demo = gr.Interface(
    fn=binary_search_visualize,
    inputs=[
        gr.Textbox(label="Sorted numbers (comma-separated)", value="1, 3, 5, 7, 9, 11, 13"),
        gr.Number(label="Target to find", value=7)
    ],
    outputs="text",
    title="Binary Search Visualizer"
)

demo.launch()
