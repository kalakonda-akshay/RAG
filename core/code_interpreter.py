"""
Local Code Interpreter and Data Visualization Engine using Matplotlib and Pandas.
"""
import os
import sys
import tempfile
import io
import contextlib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless plotting
import matplotlib.pyplot as plt


def run_code_and_plot(code_str: str) -> dict:
    """
    Executes Python code in an isolated scope and captures printed stdout and generated matplotlib figure.
    Returns: {"output": "<stdout>", "image_path": "<path or None>", "error": "<error or None>"}
    """
    cleaned_code = code_str.strip()
    if cleaned_code.startswith("```python"):
        cleaned_code = cleaned_code[9:]
    if cleaned_code.startswith("```"):
        cleaned_code = cleaned_code[3:]
    if cleaned_code.endswith("```"):
        cleaned_code = cleaned_code[:-3]
    cleaned_code = cleaned_code.strip()

    stdout_buf = io.StringIO()
    plt.close("all")  # Clear active figures

    local_vars = {}
    global_vars = {"plt": plt}

    image_path = None
    error_msg = None

    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(cleaned_code, global_vars, local_vars)

        # Check if matplotlib generated a plot
        fig = plt.gcf()
        if fig and fig.get_axes():
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
                image_path = tmp_img.name
            plt.savefig(image_path, bbox_inches="tight", dpi=150)
            plt.close("all")
    except Exception as e:
        error_msg = str(e)

    output_text = stdout_buf.getvalue().strip()
    return {
        "output": output_text,
        "image_path": image_path,
        "error": error_msg,
    }
