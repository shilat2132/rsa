
/**
 * Utilities for handling Turing machine steps and navigation
 *  * getCurrentStep -  Gets the current step from the step tree based on the path
 *  * getNextStep -  Gets the next step based on the current path
 *  * getCurrentFormula
 *  * applyStepToState
 */




/**
 * Gets the current step from the step tree based on the path
 * @returns the step object. if not found - returns null
 */
export const getCurrentStep = (stepTree, currentPath) => {
  if (!currentPath?.length || !stepTree?.steps) return null;
  
  let current = stepTree;
  let step = null;
  
  // Navigate through the path to find the current step
  for (let i = 0; i < currentPath.length; i++) {
    const index = currentPath[i];
    
    if (!current.steps || !current.steps[index]) {
      return null;
    }
    
    step = current.steps[index];
    current = step;
  }
  
  return step;
};

/**
 * Gets the next step based on the current path
 *   * @returns {
   *  * step: the next step object,
   *  * path: the path of the next step,
   *  * exiting: boolean to indicate whether the next step is still in the current submachine or there is a need to exit it
   *  * removeLevels: the num of submachines to exit
   * }
 */
export const getNextStep = (stepTree, currentPath) => {
  if (!currentPath?.length || !stepTree?.steps) return null;

  const tryResolvePath = (path) => {
    let temp = stepTree;
    for (let i = 0; i < path.length; i++) {
      const index = path[i];
      if (!temp.steps || !temp.steps[index]) return null;
      temp = temp.steps[index];
    }
    return temp;
  };

  // Check if current step is a submachine with steps
  const currentStep = getCurrentStep(stepTree, currentPath);
  if (currentStep && currentStep.action === 'submachine' && currentStep.steps && currentStep.steps.length > 0) {
    // Enter submachine
    return { step: currentStep.steps[0], path: [...currentPath, 0] };
  }

  // Try incrementing the last index (sibling in same submachine)
  let pathCopy = [...currentPath];
  pathCopy[pathCopy.length - 1] += 1;

  let tempCurrent = tryResolvePath(pathCopy);
  if (tempCurrent) {
    return { step: tempCurrent, path: pathCopy };
  }

  // Go up in the tree and track levels removed
  const exiting = true;
  let parentPath = [...currentPath];
  let removeLevels = 1;  

  while (parentPath.length > 0) {
    parentPath = parentPath.slice(0, -1); // step one level up

    if (parentPath.length === 0) break;

    const nextSiblingPath = [...parentPath];
    nextSiblingPath[nextSiblingPath.length - 1] += 1;

    tempCurrent = tryResolvePath(nextSiblingPath);
    if (tempCurrent) {
      return {
        step: tempCurrent,
        path: nextSiblingPath,
        exiting,
        removeLevels
      };
    }

    removeLevels++; 
  }

  return null;
};

/**
 * Gets the appropriate formula to display
 */
export const getCurrentFormula = (currentState, getCurrentStep) => {
  const currentStep = getCurrentStep();
  if (currentState.submachines.length > 0) {
    // Get the formula from the latest submachine
    const latestSubmachine = currentState.submachines[currentState.submachines.length - 1];
    return latestSubmachine.formula || '';
  } else if (currentStep && currentStep.formula) {
    return currentStep.formula;
  }
  return currentState.mainFormula;
};



export const applyStepToState = (step, setCurrentState, writeTimeout, writeDelay) => {
  if (!step) return;

  switch (step.action) {
    case 'main':
      break;

    case 'step':
      // First highlight positions without writing - transitionState is a prop to the submachineStack that passes one of its fields to turingTape so it rerndered each time the transitionState is changed
      setCurrentState(prev => {
        return {
          ...prev,
          transitionState: {
            positions: step.pos,
            writes: step.write,
            spaces: step.spaces
          }
        };
      });

      
      // After a delay, apply the writes (to simulate the write operation)

      // first clear the timer of the writing delay
      if (writeTimeout.current) {
        clearTimeout(writeTimeout.current);
      }
      
      writeTimeout.current = setTimeout(() => {
        setCurrentState(prev => {

          // Safely deep copy all tapes, ensuring each tape is an array
          const newTapes = (prev.tapes || []).map(tape => {
            // Ensure tape is an array before spreading
            if (Array.isArray(tape)) {
              return [...tape];
            } else {
              console.warn('Non-array tape found:', tape);
              return [];
            }
          });
          
          // Apply writes to the tapes if we have positions and values
          if (step.pos && step.write && Array.isArray(step.pos) && Array.isArray(step.write)) {
            // traverse the tapes. for each one: retrive the pos and the writing value
            for (let i = 0; i < Math.min(step.pos.length, step.write.length, newTapes.length); i++) {
              const pos = step.pos[i];
              const writeVal = step.write[i];
              
              if (typeof pos === 'number' && pos >= 0) {
                // Ensure the tape is long enough
                while (newTapes[i].length <= pos) {
                  newTapes[i].push('_');
                }
                
                // Write the new value at the position
                newTapes[i][pos] = writeVal
              }
            }
          }
          
          // Apply spaces after writing (if needed)
          if (step.spaces && Array.isArray(step.spaces)) {
            for (let i = 0; i < Math.min(step.spaces.length, newTapes.length); i++) {
              if (step.spaces[i] === -1) {
                newTapes[i].unshift('_');
                // Adjust position for the shift - update the transition state
                if (prev.transitionState?.positions && prev.transitionState.positions[i] !== undefined) {
                  prev.transitionState.positions[i] += 1;
                }
              } else if (step.spaces[i] === 1) {
                newTapes[i].push('_');
              }
            }
          }

          // update the tapes of the current active machine
          const updatedSubmachines = [...prev.activeSubmachines];
          if (updatedSubmachines.length > 0) {
            const lastIndex = updatedSubmachines.length - 1;
            updatedSubmachines[lastIndex] = {
              ...updatedSubmachines[lastIndex],
              tapes: newTapes
            };
          }
          return {
            ...prev,
            activeSubmachines: updatedSubmachines,
            tapes: newTapes,
            transitionState: {
              positions: step.pos, // Keep the updated positions
              writeCompleted: true
            }
          };
        });
      }, writeDelay.current);
     
      break;
      
   case 'updateTape':
  setCurrentState(prev => {
    const newTapes = Array.isArray(prev.tapes) ? [...prev.tapes] : [];

    if (step.tape_index < newTapes.length && Array.isArray(step.tape)) {
      newTapes[step.tape_index] = [...step.tape]; // Deep copy
    }

    // Update also the tape in the active submachine
    const updatedSubmachines = [...prev.activeSubmachines];
    if (updatedSubmachines.length > 0) {
      const lastIndex = updatedSubmachines.length - 1;
      const updatedSubmachine = { ...updatedSubmachines[lastIndex] };

      if (Array.isArray(updatedSubmachine.tapes)) {
        const updatedSubTapes = [...updatedSubmachine.tapes];
        if (step.tape_index < updatedSubTapes.length) {
          updatedSubTapes[step.tape_index] = [...step.tape];
        }
        updatedSubmachine.tapes = updatedSubTapes;
      }

      updatedSubmachines[lastIndex] = updatedSubmachine;
    }

    return { 
      ...prev, 
      tapes: newTapes,
      activeSubmachines: updatedSubmachines,
      transitionState: null 
    };
  });
  break;


    case 'updateMachine':
  setCurrentState(prev => {
    const updatedTapes = step.tapes && Array.isArray(step.tapes) ?
      step.tapes.map(tape => Array.isArray(tape) ? [...tape] : []) :
      prev.tapes || [];

    const updatedSubmachines = [...prev.activeSubmachines];
    if (updatedSubmachines.length > 0) {
      const lastIndex = updatedSubmachines.length - 1;
      updatedSubmachines[lastIndex] = {
        ...updatedSubmachines[lastIndex],
        tapes: updatedTapes
      };
    }

    return {
      ...prev,
      tapes: updatedTapes,
      activeSubmachines: updatedSubmachines,
      transitionState: null
    };
  });
  break;

      

      
    case 'submachine':
      // Handled by enterSubmachine
      break;

    default:
      console.warn('Unknown step action:', step.action);
  }
};

