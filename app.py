import os
import shutil
import subprocess
import streamlit as st

st.set_page_config(
    page_title="C-Subset Compiler Front-End", page_icon="⚙️", layout="wide"
)

st.title("⚙️ C-Subset Compiler Front-End Explorer")
st.markdown(
    "Interactive Lexical and Syntax Analyzer powered by **Flex**, **Bison (Yacc)**, and a custom scoped **Symbol Table**."
)


@st.cache_resource
def build_compiler():
  """Compiles the Flex and Bison parser binary."""
  try:
    # Ensure any previous custom header name is also available
    # 1. Run Bison to generate y.tab.c and y.tab.h
    bison_res = subprocess.run(
        ["bison", "-d", "-y", "parser.y"], capture_output=True, text=True
    )
    if bison_res.returncode != 0:
      return False, f"Bison Error:\n{bison_res.stderr}"

    # Also create a copy as 22101869.tab.h just in case lexer.l still references it
    if os.path.exists("y.tab.h"):
      shutil.copy("y.tab.h", "22101869.tab.h")

    # 2. Run Flex to generate lex.yy.c
    flex_res = subprocess.run(
        ["flex", "-o", "lex.yy.c", "lexer.l"],
        capture_output=True,
        text=True,
    )
    if flex_res.returncode != 0:
      return False, f"Flex Error:\n{flex_res.stderr}"

    # 3. Compile and Link with g++
    compile_cmd = [
        "g++",
        "-w",
        "-std=c++11",
        "y.tab.c",
        "lex.yy.c",
        "-o",
        "compiler",
    ]
    gcc_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    if gcc_res.returncode != 0:
      return False, f"G++ Compilation Error:\n{gcc_res.stderr}"

    return True, "Compiler built successfully!"
  except Exception as e:
    return False, f"Execution failed: {str(e)}"


# Build status
with st.spinner("Compiling Lexer & Parser binaries..."):
  success, msg = build_compiler()

if not success:
  st.error(msg)
  st.stop()

col_left, col_right = st.columns([1, 1])

# Sample source code
default_code = """int a, b, c;
float x;

int main() {
    a = 10;
    b = 20;
    c = a + b * 2;
    if (c > 30) {
        x = 3.14;
    }
    return 0;
}
"""

if os.path.exists("input.txt"):
  try:
    with open("input.txt", "r") as f:
      sample_file = f.read().strip()
      if sample_file:
        default_code = sample_file
  except Exception:
    pass

with col_left:
  st.subheader("Source Code Input")
  source_code = st.text_area(
      "Write or paste your C-subset code:",
      value=default_code,
      height=380,
      help="Input C code to run through the lexical and syntax parser.",
  )
  run_button = st.button("Parse & Analyze", type="primary")

with col_right:
  st.subheader("Compiler Output & Diagnostics")

  if run_button or source_code:
    with open("temp_input.txt", "w") as f:
      f.write(source_code)

    try:
      result = subprocess.run(
          ["./compiler", "temp_input.txt"],
          capture_output=True,
          text=True,
          timeout=5,
      )

      tabs = st.tabs(["Parser Log / Tokens", "Standard Output", "Errors"])

      with tabs[0]:
        output_found = False
        for fname in ["log.txt", "parser_log.txt", "symbol_table.txt"]:
          if os.path.exists(fname):
            with open(fname, "r") as f:
              st.code(f.read(), language="text")
            output_found = True
            break
        if not output_found:
          if result.stdout.strip():
            st.code(result.stdout, language="text")
          else:
            st.info("Parsing completed.")

      with tabs[1]:
        if result.stdout.strip():
          st.code(result.stdout, language="text")
        else:
          st.info("No console stdout.")

      with tabs[2]:
        if os.path.exists("error.txt") and os.path.getsize("error.txt") > 0:
          with open("error.txt", "r") as f:
            st.error(f.read())
        elif result.stderr.strip():
          st.error(result.stderr)
        else:
          st.success("No syntax errors detected! Grammar validation passed.")

    except subprocess.TimeoutExpired:
      st.error("Execution timed out.")
    except Exception as e:
      st.error(f"Execution error: {str(e)}")
