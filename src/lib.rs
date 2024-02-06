use pyo3::prelude::*;
use std::collections::{HashSet, LinkedList};

#[pyclass]
struct Graph {
    vertices: Vec<Vec<u32>>,
}

#[pymethods]
impl Graph {
    #[new]
    fn new(vertices: Vec<Vec<u32>>) -> Self {
        Graph { vertices }
    }

    #[staticmethod]
    fn new_grid(rows: u32, cols: u32) -> Self {
        let mut graph = Graph {
            vertices: Vec::with_capacity(rows as usize),
        };

        for row in 0..rows {
            for col in 0..cols {
                let mut vertices = Vec::new();

                if row > 0 {
                    vertices.push(1 + (row - 1) * cols + col);
                }
                if col > 0 {
                    vertices.push(1 + row * cols + col - 1);
                }
                if col + 1 < cols {
                    vertices.push(1 + row * cols + col + 1);
                }
                if row + 1 < rows {
                    vertices.push(1 + (row + 1) * cols + col);
                }

                graph.vertices.push(vertices);
            }
        }

        graph
    }

    #[getter]
    fn get_vertices(&self) -> PyResult<Vec<Vec<u32>>> {
        Ok(self.vertices.clone())
    }

    #[setter]
    fn set_vertices(&mut self, vertices: Vec<Vec<u32>>) {
        self.vertices = vertices;
    }

    fn longest_elementary_paths(&self, start: u32, end: u32) -> PyResult<Option<Vec<Vec<u32>>>> {
        if start > self.vertices.len() as u32 || end > self.vertices.len() as u32 {
            return Ok(None);
        }

        let mut solutions = Vec::new();
        let mut visited = HashSet::new();
        let mut path = LinkedList::new();
        visited.insert(start);
        path.push_back(start);

        fn lep(
            solutions: &mut Vec<LinkedList<u32>>,
            visited: &mut HashSet<u32>,
            path: &mut LinkedList<u32>,
            graph: &Graph,
            end_node: u32,
        ) {
            let current_node = *path.back().unwrap();

            for next_node in graph.vertices[(current_node - 1) as usize].iter() {
                let next_node = *next_node;
                if visited.insert(next_node) {
                    path.push_back(next_node);

                    if next_node == end_node {
                        solutions.push(path.clone());
                    } else {
                        lep(solutions, visited, path, graph, end_node);
                    }

                    visited.remove(&next_node);
                    path.pop_back();
                }
            }
        }

        lep(&mut solutions, &mut visited, &mut path, &self, end);

        match Graph::filter_longest_paths(solutions) {
            Some(solutions) => {
                let solutions: Vec<Vec<u32>> = solutions
                    .into_iter()
                    .map(|linked_list| linked_list.into_iter().collect())
                    .collect();
                Ok(Some(solutions))
            }
            None => Ok(None),
        }
    }


    fn longest_simple_paths(&self, start: u32, end: u32) -> PyResult<Option<Vec<Vec<u32>>>> {
        if start > self.vertices.len() as u32 || end > self.vertices.len() as u32 {
            return Ok(None);
        }

        let mut solutions = Vec::new();
        let mut visited = HashSet::new();
        let mut path = LinkedList::new();
        path.push_back(start);

        fn lsp(
            solutions: &mut Vec<LinkedList<u32>>,
            visited: &mut HashSet<(u32, u32)>,
            path: &mut LinkedList<u32>,
            graph: &Graph,
            end_node: u32,
        ) {
            let current_node = *path.back().unwrap();

            for next_node in graph.vertices[(current_node - 1) as usize].iter() {
                let next_node = *next_node;
                if !visited.contains(&(next_node, current_node))
                    && visited.insert((current_node, next_node))
                {
                    path.push_back(next_node);

                    if next_node == end_node {
                        solutions.push(path.clone());
                    } else {
                        lsp(solutions, visited, path, graph, end_node);
                    }

                    visited.remove(&(current_node, next_node));
                    path.pop_back();
                }
            }
        }

        lsp(&mut solutions, &mut visited, &mut path, &self, end);

        match Graph::filter_longest_paths(solutions) {
            Some(solutions) => {
                let solutions: Vec<Vec<u32>> = solutions
                    .into_iter()
                    .map(|linked_list| linked_list.into_iter().collect())
                    .collect();
                Ok(Some(solutions))
            }
            None => Ok(None),
        }
    }
}

impl Graph {
    fn filter_longest_paths(paths: Vec<LinkedList<u32>>) -> Option<Vec<LinkedList<u32>>> {
        if paths.is_empty() {
            return None;
        }

        let longest_path_vertex_count = paths.iter().map(|l| l.len()).max()?;
        let solutions = paths
            .into_iter()
            .filter(|l| l.len() == longest_path_vertex_count)
            .collect();
        Some(solutions)
    }
}

#[pymodule]
fn taksioras(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Graph>()?;
    Ok(())
}

#[test]
fn simple() {
    let graph = Graph::new_grid(3, 3);
    let paths = graph.longest_simple_paths(1, 9);
    print(paths);
}

#[test]
fn elementary() {
    let graph = Graph::new_grid(3, 3);
    let paths = graph.longest_elementary_paths(1, 9);
    print(paths);
}

fn print(paths: PyResult<Option<Vec<Vec<u32>>>>) {
    let Ok(paths) = paths else {
        return;
    };
    if let Some(paths) = paths {
        for path in paths {
            let mut path = path.into_iter();
            if let Some(vertex) = path.next() {
                print!("{vertex}");
                for vertex in path {
                    print!("->{vertex}");
                }
                println!()
            }
        }
    } else {
        println!("Nerasta kelių");
    }
}