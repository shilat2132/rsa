
/**
 * Inserts simulation steps from a chunk into a nested step tree structure,
 * and removes empty placeholders once all chunk steps are inserted.
 *
 * @param {Object} currentTree - The existing step tree.
 * @param {Array} chunk - An array of tuples: [path: number[], step: object]
 * @returns {Object} - Updated and cleaned step tree.
 */
export const processChunk = (currentTree, chunk) => {
  if (!chunk || !Array.isArray(chunk) || chunk.length === 0) {
    return currentTree;
  }

  // Deep copy to avoid mutating the original tree
  const newTree = structuredClone(currentTree || {});

  // chunk is an array in the following format: [path: [0, 3, 4], step: the object step for either: main, regular step, updateTape, updateMachine or submachine]
  chunk.forEach(([path, step]) => {
    // the main (root) step has a path of []
    if (path.length === 0) {
      const enrichedRoot = {
        // ...newTree,
        ...step
      };

      if ('steps' in step && !Array.isArray(enrichedRoot.steps)) {
        enrichedRoot.steps = [];
      }

      Object.assign(newTree, enrichedRoot); //keeps the referance to the original newTree
      return;
    }

    let current = newTree;

    // Traverse the path except the last index
    for (let i = 0; i < path.length - 1; i++) {
      const index = path[i];

      // each level in the path (except the last one) is a submachine - therefore should have steps field
      if (!current.steps) {
        current.steps = [];
      }

      // in case that prior steps were sent in preceeding chunks and now their cells are undefined 
      // - initialize them with an empty object (will be deleted at the end of the tree construction)
      while (current.steps.length <= index) {
        current.steps.push({}); 
      }

      current = current.steps[index];
    }

    // Final level: insert the step
    const finalIndex = path[path.length - 1];

    if (!current.steps) {
      current.steps = [];
    }

    while (current.steps.length <= finalIndex) {
      current.steps.push({}); 
    }

    const enrichedStep = {
      ...current.steps[finalIndex],
      ...step
    };

    // Only create a `steps` array if the step actually includes one
    if ('steps' in step && !Array.isArray(enrichedStep.steps)) {
      enrichedStep.steps = [];
    }

    current.steps[finalIndex] = enrichedStep;
  });

  // Clean up placeholders: remove empty {} from all `steps` arrays
  cleanEmptySteps(newTree);
  // console.log("current", newTree)

  return newTree;
};

/**
 * Recursively removes empty placeholder objects {} from `steps` arrays.
 *
 * @param {Object|Array} node - Node in the tree to clean.
 */
function cleanEmptySteps(node) {
  if (!node || typeof node !== 'object') return;

  if (Array.isArray(node)) {
    for (let i = 0; i < node.length; i++) {
      cleanEmptySteps(node[i]);
    }
    return;
  }

  if (Array.isArray(node.steps)) {
    node.steps = node.steps
      .map(step => {
        cleanEmptySteps(step);
        return step;
      })
      .filter(
        step =>
          !(step && typeof step === 'object' && Object.keys(step).length === 0)
      );
  }

  // Clean deeper nested fields.
  for (const key in node) {
    if (typeof node[key] === 'object') {
      cleanEmptySteps(node[key]);
    }
  }
}

/**
 * Extract all tapes from a step or machine
 * @param {Object} step - A step with possible tapes
 * @returns {Array} - Array of tapes
 */
export const extractTapes = (step) => {
  if (!step) return [];
  
  if (step.tapes && Array.isArray(step.tapes)) {
    return step.tapes;
  }
  
  return [];
};

/**
 * Find step at a specific path in the step tree
 * @param {Object} tree - The step tree
 * @param {Array} path - Path to the step (array of indices)
 * @returns {Object|null} - The step at the path, or null if not found
 */
export const findStepAtPath = (tree, path) => {
  if (!tree || !path || path.length === 0) {
    return tree; // Return the tree itself if path is empty
  }
  
  let current = tree;
  
  for (let i = 0; i < path.length; i++) {
    const index = path[i];
    
    if (!current.steps || !current.steps[index]) {
      return null;
    }
    
    current = current.steps[index];
  }
  
  return current;
};

/**
 * Get the next step path in the tree
 * @param {Object} tree - The step tree
 * @param {Array} currentPath - Current path of indices
 * @returns {Array|null} - Next path or null if end reached
 */
export const getNextStepPath = (tree, currentPath) => {
  if (!tree || !currentPath) {
    return [0]; // Start with the first step if no path provided
  }

  // Try incrementing the last index (which will imply that we're still in the same submachine) and check 
  // if this path exists in the tree
  const newPath = [...currentPath];
  newPath[newPath.length - 1] += 1;
  
  // Check if this path exists
  if (findStepAtPath(tree, newPath)) {
    return newPath;
  }
  
  // Check if we need to enter a submachine
  const currentStep = findStepAtPath(tree, currentPath);
  if (currentStep && currentStep.action === 'submachine' && currentStep.steps && currentStep.steps.length > 0) {
    // Enter submachine by adding a 0 to the path
    return [...currentPath, 0];
  }
  
  // If we're in a submachine and reached the end, check if there's a parent
  if (currentPath.length > 1) {
    // Go up one level and increment
    const parentPath = currentPath.slice(0, -1);
    parentPath[parentPath.length - 1] += 1;
    
    // Check if this parent-level path exists
    if (findStepAtPath(tree, parentPath)) {
      return parentPath;
    }
    
    // If not, try going up further
    return getNextStepPath(tree, currentPath.slice(0, -1));
  }
  
  return null; // No next step found
};
