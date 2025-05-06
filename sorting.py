import tkinter as tk
from tkinter import ttk
import random
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("800x600")  # Increased window height for better spacing
        self.root.config(bg="white")

        self.data = []
        self.speed = 0.2  # Increased speed for slower visualization (in seconds)
        self.sorting = False  # Flag to track if sorting is active

        # Heading
        heading = tk.Label(self.root, text="Sorting Algorithm Visualizer", font=("Helvetica", 20, "bold"), bg="white")
        heading.pack(pady=10)

        # UI Frame (Buttons and Dropdown)
        ui_frame = tk.Frame(self.root, width=800, height=100, bg="lightgray")
        ui_frame.pack(padx=10, pady=5)

        # Dropdown for selecting sorting algorithm
        self.sorting_algorithm = ttk.Combobox(ui_frame, values=["Bubble Sort", "Quick Sort", "Selection Sort", "Merge Sort", "Insertion Sort"], width=20)
        self.sorting_algorithm.set("Select Sorting Algorithm")
        self.sorting_algorithm.grid(row=0, column=0, padx=10, pady=10)
        self.sorting_algorithm.bind("<<ComboboxSelected>>", self.update_explanation)  # Update explanation on selection

        # Buttons
        tk.Button(ui_frame, text="Generate Data", command=self.generate_data, bg="blue", fg="white").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(ui_frame, text="Execute", command=self.execute_sorting, bg="green", fg="white").grid(row=0, column=2, padx=10, pady=10)
        tk.Button(ui_frame, text="Stop Sorting", command=self.stop_sorting, bg="gray", fg="white").grid(row=0, column=3, padx=10, pady=10)

        # Explanation Label
        self.explanation_label = tk.Label(self.root, text="Select a sorting algorithm to view its explanation", font=("Arial", 12), bg="white", wraplength=700, justify="left")
        self.explanation_label.pack(pady=10)

        # Canvas for chart
        self.canvas = tk.Canvas(self.root, width=780, height=300, bg="white")
        self.canvas.pack(padx=10, pady=20)  # Added more padding between chart and buttons

    def update_explanation(self, event):
        selected_algorithm = self.sorting_algorithm.get()

        explanations = {
            "Bubble Sort": "Bubble Sort repeatedly compares adjacent elements and swaps them if they are in the wrong order. Example: [5, 2, 9, 1] -> [2, 5, 9, 1] -> [2, 5, 1, 9]...",
            "Quick Sort": "Quick Sort divides the list into smaller parts using a pivot, and sorts them individually. Example: [10, 7, 8, 9, 1, 5] -> Pivot 5 -> [1, 5, 8, 9, 7, 10]...",
            "Selection Sort": "Selection Sort finds the smallest element in the unsorted part and swaps it with the first unsorted element. Example: [64, 25, 12, 22, 11] -> [11, 25, 12, 22, 64]...",
            "Merge Sort": "Merge Sort splits the list into halves, recursively sorts each half, and merges them back together in sorted order. Example: [38, 27, 43, 3, 9, 82, 10] -> [3, 9, 10, 27, 38, 43, 82]...",
            "Insertion Sort": "Insertion Sort builds the sorted list by inserting each element into its correct position. Example: [12, 11, 13, 5, 6] -> [11, 12, 13, 5, 6] -> [11, 12, 5, 13, 6]..."
        }

        # Update the explanation label with the selected algorithm's explanation
        self.explanation_label.config(text=explanations.get(selected_algorithm, "Select a sorting algorithm to view its explanation"))

    def generate_data(self):
        self.stop_sorting()
        self.data = [random.randint(10, 100) for _ in range(10)]  # Only 10 numbers
        self.draw_data(self.data, ['blue' for _ in range(len(self.data))])

    def stop_sorting(self):
        self.sorting = False  # Stop sorting when called

    def draw_data(self, data, color_array):
        if not self.canvas.winfo_exists():
            return

        try:
            self.canvas.delete("all")
            c_height = 300
            c_width = 780
            bar_width = c_width / (len(data) * 1.5)  # Adjust the bar width for spacing
            offset = 20
            spacing = 10  # Set spacing between bars
            normalized_data = [i / max(data) for i in data]

            # Drawing bars with space in between
            for i, height in enumerate(normalized_data):
                x0 = i * (bar_width + spacing) + offset  # Calculate the x position with spacing
                y0 = c_height - height * 260
                x1 = x0 + bar_width
                y1 = c_height

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])

                # Center-align the text inside the bar
                self.canvas.create_text(x0 + bar_width / 2, y0 + (y1 - y0) / 2, text=str(data[i]), font=("Arial", 10))

            self.root.update_idletasks()
        except tk.TclError:
            pass

    # Execute the selected sorting algorithm
    def execute_sorting(self):
        selected_algorithm = self.sorting_algorithm.get()
        if selected_algorithm == "Bubble Sort":
            self.bubble_sort()
        elif selected_algorithm == "Quick Sort":
            self.quick_sort()
        elif selected_algorithm == "Selection Sort":
            self.selection_sort()
        elif selected_algorithm == "Merge Sort":
            self.merge_sort()
        elif selected_algorithm == "Insertion Sort":
            self.insertion_sort()
        else:
            print("Please select a valid algorithm.")

    # Bubble Sort
    def bubble_sort(self):
        if not self.data:
            return

        self.sorting = True
        data = self.data
        n = len(data)

        for i in range(n):
            if not self.sorting:
                break
            for j in range(n - i - 1):
                if not self.sorting:
                    break

                color_array = ['red' if x == j or x == j + 1 else 'blue' for x in range(n)]
                self.draw_data(data, color_array)
                time.sleep(self.speed + 0.1)  # Slightly slower for red

                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.draw_data(data, color_array)
                    time.sleep(self.speed + 0.1)  # Slower after swapping

            self.draw_data(data, ['green' if x >= n - i - 1 else 'blue' for x in range(n)])

        if self.sorting:
            self.draw_data(data, ['green'] * len(data))
        self.sorting = False

    # Quick Sort
    def quick_sort(self):
        self.sorting = True
        self.quick_sort_helper(self.data, 0, len(self.data) - 1)
        self.sorting = False

    def quick_sort_helper(self, data, low, high):
        if low < high:
            pi = self.partition(data, low, high)

            self.draw_data(data, ['red' if i == pi else 'blue' for i in range(len(data))])
            time.sleep(self.speed + 0.1)
            self.quick_sort_helper(data, low, pi - 1)
            self.quick_sort_helper(data, pi + 1, high)

    def partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                self.draw_data(data, ['blue' for _ in range(len(data))])
                time.sleep(self.speed + 0.1)
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1

    # Selection Sort
    def selection_sort(self):
        self.sorting = True
        data = self.data
        n = len(data)

        for i in range(n):
            if not self.sorting:
                break
            min_idx = i
            for j in range(i + 1, n):
                if not self.sorting:
                    break
                if data[j] < data[min_idx]:
                    min_idx = j
                self.draw_data(data, ['red' if x == i or x == min_idx else 'blue' for x in range(n)])
                time.sleep(self.speed + 0.1)
            data[i], data[min_idx] = data[min_idx], data[i]
            self.draw_data(data, ['green' if x <= i else 'blue' for x in range(n)])

        if self.sorting:
            self.draw_data(data, ['green'] * len(data))
        self.sorting = False

    # Merge Sort
    def merge_sort(self):
        self.sorting = True
        self.merge_sort_helper(self.data)
        self.sorting = False

    def merge_sort_helper(self, data):
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = self.merge_sort_helper(data[:mid])
        right = self.merge_sort_helper(data[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # Insertion Sort
    def insertion_sort(self):
        self.sorting = True
        data = self.data
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1

            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
            self.draw_data(data, ['red' if x == j + 1 else 'blue' for x in range(len(data))])
            time.sleep(self.speed + 0.1)

        self.draw_data(data, ['green'] * len(data))
        self.sorting = False

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
