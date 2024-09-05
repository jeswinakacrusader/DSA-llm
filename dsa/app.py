import streamlit as st
from langchain_ollama import OllamaLLM
import re

# Initialize the language model
model = OllamaLLM(model="codellama:7b")

def is_valid_dsa_question(question):
    # Define keywords that indicate a valid DSA question
    dsa_keywords = [
        "array", "linked list", "tree", "graph", "sorting", "searching", 
        "dynamic programming", "stack", "queue", "doubly linked list", 
        "hash table", "binary search", "recursion", "stack implementation", 
        "queue implementation", "infix to postfix", "balanced parentheses", 
        "stock span problem", "next greater element", "binary tree", 
        "binary search tree", "depth-first search", "breadth-first search", 
        "dijkstra's algorithm", "kruskal's algorithm", "prim's algorithm", 
        "topological sort", "longest common subsequence", "knapsack problem", 
        "merge sort", "quicksort", "heapsort", "radix sort", "trie", 
        "suffix array", "segment tree", "fenwick tree", "union-find", 
        "sliding window", "two pointers", "greedy algorithm", "divide and conquer", 
        "backtracking", "memoization", "bit manipulation", "mp3 player", 
        "doubly linked list mp3 player", "playback controls", "playlist management"
    ]
    return any(keyword in question.lower() for keyword in dsa_keywords)


def clean_response(response):
    # Remove code snippets enclosed in triple backticks
    cleaned_response = re.sub(r'```.*?```', '', response, flags=re.DOTALL)
    return cleaned_response.strip()

def generate_question(topic=None):
    question = f"""You are an interactive DSA coding questions bot specializing in generating challenging Python Data Structures and Algorithms questions. 
    Please provide a detailed question that includes:
    Problem Statement: A clear description of the problem to be solved.
    Input/Output Specifications: Define the format for the input and output.
    Constraints: Specify any constraints or limitations relevant to the problem.
    Example: Include one or more examples with input and expected output.
    Ensure that the question is both challenging and relevant to advanced DSA topics. 
    {'Topic: ' + topic if topic else ''}
    """
    response = model.invoke(question)
    return response

def run_llm(prompt):
    try:
        response = model.invoke(prompt)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def solve_question():
    st.markdown("### Type the Question")
    question = st.text_area("Enter your DSA question here:", height=200, key="question")

    if st.button("Submit"):  # Submit button for the question
        if not question.strip():
            st.warning("Please enter a valid question.")
        elif not is_valid_dsa_question(question):
            st.warning("The question must relate to DSA topics like arrays, trees, sorting, linked lists, stacks, queues, or other advanced concepts. Please revise your question.")
        else:
            prompt = f'''
            You are a DSA question solving assistant using Python. You can solve any Python DSA questions or programs related to a wide range of topics, including:

1. Implement and manipulate arrays, linked lists, stacks, queues, trees, graphs, hash tables, and other data structures without any code snippets.
2. Perform sorting algorithms like merge sort, quicksort, heapsort, and radix sort without any code snippets.
3. Implement searching algorithms such as binary search and depth-first/breadth-first search without any code snippets.
4. Solve dynamic programming problems, including the knapsack problem and longest common subsequence without any code snippets.
5. Implement greedy algorithms, divide and conquer strategies, and backtracking techniques without any code snippets.
6. Solve problems related to bit manipulation, sliding window, two pointers, and more without any code snippets.
7. Implement advanced data structures like tries, suffix arrays, segment trees, and Fenwick trees without any code snippets.
8. Apply graph algorithms such as Dijkstra's, Kruskal's, Prim's, and topological sort without any code snippets.
9. Implement an MP3 player using a doubly linked list, including features like:
   - Track management (add, remove, play, pause, next, previous)
   - Playlist functionality
   - User interface for playback controls
10. You are an expert in linked lists, a fundamental dynamic data structure. A linked list consists of a series of nodes, each containing two key components: data and a reference (or pointer) to the next node in the sequence. This design enables efficient insertion and deletion operations, as elements are not required to be stored in contiguous memory locations.
Your task is to provide detailed explanations, comparisons, and practical applications of linked lists, highlighting their advantages and disadvantages in various programming contexts. This version uses bold formatting to emphasize key terms, making the prompt more engaging and visually appealing.

11. Please classify the problem, generate the corresponding Python program **without any code snippets**. 
generate the response 
Problem: {question}
            '''
            with st.spinner('Fetching response...'):
                response = run_llm(prompt)
                if response:
                    st.markdown("### Solution:")
                    st.code(response, language='python')
                else:
                    st.error("Failed to fetch a response.")
            st.success('Response received!')

def interactive_problem_solving():
    st.markdown("### Interactive Problem Solving")

    with st.spinner('Fetching Question...'):
        question = generate_question()
        st.write(question)

    user_answer = st.text_area("Write the solution:", height=300, key="interactive_implementation")
    if st.button("Submit Solution"):  # Submit button for the solution
        with st.spinner('Evaluating your solution...'):
            # Here you can implement evaluation logic
            st.write("Your solution has been submitted!")

def main():
    st.set_page_config(page_title="DSA.Ai", layout="wide")
    st.title("DSA.ai")

    st.markdown("### Instructions")
    st.write("Please enter a valid DSA question related to topics such as arrays, trees, sorting, linked lists, stacks, queues, or other advanced concepts, including implementing an MP3 player using a doubly linked list.")

    with st.sidebar:
        st.image("logo.png", use_column_width=True)
        option = st.radio("Choose a section", ["Solve", "Practice"])

    if option == "Solve":
        solve_question()
    
    st.markdown(
        """
        <style>
        .footer {
            position: absolute;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
