# A program which finds and animates the longest path on a graph

## Made for KTU's Discrete Structures course
## No requirements.txt is provided, so you will be on your own when setting up the Python environment

### This program finds the longest path in a provided graph.
The program provides a GUI in which various parameters can in set:
- Graph type (grid or adjacency list)
- Start vertex
- End vertex
- Whether to find elementary paths (a vertex shall not appear more than once in the path) or simple paths (an edge may not appear more than once in the path)

### UI
<img width="864" height="902" alt="image" src="https://github.com/user-attachments/assets/d39fa9e3-4e92-4c90-abe0-bac30dee73fb" />
<img width="865" height="899" alt="image" src="https://github.com/user-attachments/assets/9df91eb0-9fe5-4eda-a4be-bbe1e6b4d969" />

### Resulting paths
<img width="798" height="837" alt="image" src="https://github.com/user-attachments/assets/87c96dc8-f568-4aa1-b316-2db1852372b2" />
<img width="864" height="905" alt="image" src="https://github.com/user-attachments/assets/81881c6d-bf6c-4eb9-9900-703f649ffd54" />

### Architecture
The path solver is written in Rust and the UI is created using Python. This is achieved via the PyO3 project.
The main justification for this dual language architecture is for speeding up path solving.
