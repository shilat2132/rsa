import { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { getCurrentStep as getStepFromPath, getNextStep as getNextStepFromPath, getCurrentFormula, applyStepToState } from '../utils/operations/turingStepUtils';
import SubmachineStack from './SubmachineStack';
import MainMachineTapes from './MainMachineTapes';

/**
 * TuringMachine component
 * Renders a visualization of the Turing machine with tapes, handles step animation
 */
const TuringMachine = forwardRef(({ stepTree, isRunning, setSimulationState, speed, currentPath = [0], isFinished }, ref) => {
  // Current state of the machine
  const [currentState, setCurrentState] = useState({
    tapes: [],
    currentPath: currentPath || [0], // Path to current step in the tree
    animating: false,
    submachines: [], // Stack of active submachines
    mainFormula: '', // Store the main formula to display at all times
    activeSubmachines: [], // Active submachines for visualization
    stepHistory: [], // History of paths for back navigation
    transitionState: null, // For step animation
    submachineNextStep: null, // For handling submachine exit steps
    stepTree // Store the step tree in the state
  });
  
  // Animation timing
  const stepDuration = useRef(1000 / speed);
  const writeDelay = useRef(stepDuration.current * 0.5); // Half step duration for write delay
  const animationTimeout = useRef(null);
  const writeTimeout = useRef(null);
  
  // Expose methods to parent component via ref
  useImperativeHandle(ref, () => ({
    handleFullRestart: () => handleFullRestart(),
    stepForward: () => stepForward()
  }));
  
  // Initialize when stepTree changes
  useEffect(() => {
    if (stepTree && stepTree.steps && stepTree.steps.length > 0) {
      // Initialize with the main step's tapes
      
      const mainStep = stepTree.steps[0];
      setCurrentState({
        tapes: mainStep.tapes ? mainStep.tapes.map(tape => [...tape]) : [],
        currentPath:  [0], 
        animating: false,
        submachines: [],
        mainFormula: mainStep.formula || '',
        activeSubmachines: [],
        stepHistory: [],
        transitionState: null,
        submachineNextStep: null,
        stepTree // Add step tree to state
      });
    }
 

  }, [stepTree]);



  // Update step duration and write delay when speed changes
  useEffect(() => {
    stepDuration.current = 1000 / speed;
    writeDelay.current = stepDuration.current * 0.5;
  }, [speed]);

  // Update current path when prop changes
  // props of current path changes when the user clicks step forward/back - fetches chunks if they are finished
  useEffect(() => {
    if (currentPath && currentPath.length > 0) {
      setCurrentState(prev => {
        // Save the previous path for step back capability
        const newHistory = [...prev.stepHistory];
        if (prev.currentPath.toString() !== currentPath.toString()) {
          newHistory.push(prev.currentPath);
        }
        
        return {
          ...prev,
          currentPath: currentPath,
          stepHistory: newHistory
        };
      });
      
      // Apply the current step to update the visualization
      const currentStep = getCurrentStep();
      if (currentStep) {
        applyStep(currentStep);
      }
    }
  }, [currentPath]);

  // Handle play/pause of animation
  // when the user toggle play/pause the isRunning prop changes
  // this effect sets the animating state according to the user's choice and clears timers
  useEffect(() => {
    if (isRunning && !currentState.animating) {
      // Start animation
      setCurrentState(prev => ({ ...prev, animating: true }));
    } else if (!isRunning && currentState.animating) {
      // Stop animation
      if (animationTimeout.current) {
        clearTimeout(animationTimeout.current);
        animationTimeout.current = null;
      }
      if (writeTimeout.current) {
        clearTimeout(writeTimeout.current);
        writeTimeout.current = null;
      }
      setCurrentState(prev => ({ ...prev, animating: false }));
    }
    
    return () => {
      if (animationTimeout.current) {
        clearTimeout(animationTimeout.current);
      }
      if (writeTimeout.current) {
        clearTimeout(writeTimeout.current);
      }
    };
  }, [isRunning, currentState.animating]);

  

  // Apply step to current state with proper animation
  const applyStep = (step) => {
    applyStepToState(step, setCurrentState, writeTimeout, writeDelay);
  };

  // Enter a submachine
  const enterSubmachine = (submachineStep) => {
    setCurrentState(prev => {
      // Add current context to submachine stack
      const newSubmachines = [...prev.submachines, {
        parentPath: prev.currentPath,
        tapes: prev.tapes,
        formula: submachineStep.formula || ''
      }];
      
      // Create new active submachine
      const newActiveSubmachine = {
        level: newSubmachines.length,
        formula: submachineStep.formula || '',
        tapes: submachineStep.tapes || []
      };
      
      // Set path to first step inside submachine
      const newPath = [...prev.currentPath, 0]
      
      return {
        ...prev,
        submachines: newSubmachines,
        currentPath: newPath, 
        tapes: submachineStep.tapes || prev.tapes,
        activeSubmachines: [...prev.activeSubmachines, newActiveSubmachine],
        // Add entry path to history for back navigation
        stepHistory: [...prev.stepHistory, prev.currentPath]
      };
    });

    const currentStep = getCurrentStep();
    if (currentState.animating) {
      if (currentStep && currentStep.action !== 'submachine') {
          applyStep(currentStep);
        }
    }
  };

  /** Exit a submachine, sets the next step's path to current path, pops the submachines from the stack according to removeLevels
   * 
   */
  const exitSubmachine = (nextStepInfo) => {
    setCurrentState(prev => {
      if (prev.submachines.length === 0) return prev;
      
      const removeLevels = nextStepInfo.removeLevels || 1
      // Get the parent context
      const submachineContext = prev.submachines[prev.submachines.length - removeLevels];
      
      return {
        ...prev,
        submachines: prev.submachines.slice(0, -removeLevels), // Pop the top submachine
        currentPath: nextStepInfo ? nextStepInfo.path : submachineContext.parentPath,
        tapes: submachineContext.tapes, // Restore parent tapes
        activeSubmachines: prev.activeSubmachines.slice(0, -removeLevels), // Remove the last active submachine
        // Add exit path to history
        stepHistory: [...prev.stepHistory, prev.currentPath],
        submachineNextStep: null
      };
    });


// Continue animation after a delay
const currentStep = getCurrentStep()
    if (currentState.animating) {
      if (currentStep) {
          applyStep(currentStep);
        }
      
    }
  };

  // Handle full simulation restart
  const handleFullRestart = () => {
    // Clear any ongoing animations
    if (animationTimeout.current) {
      clearTimeout(animationTimeout.current);
      animationTimeout.current = null;
    }
    if (writeTimeout.current) {
      clearTimeout(writeTimeout.current);
      writeTimeout.current = null;
    }

    // Reset everything to initial state
    if (stepTree && stepTree.steps && stepTree.steps.length > 0) {
      const mainStep = stepTree.steps[0];
      setCurrentState({
        tapes: mainStep.tapes ? mainStep.tapes.map(tape => [...tape]) : [],
        currentPath: [0], // Reset to first step
        animating: false,
        submachines: [], // Clear all submachines
        mainFormula: mainStep.formula || '',
        activeSubmachines: [], // Clear active submachines
        stepHistory: [],
        transitionState: null,
        submachineNextStep: null,
        stepTree
      });
    }

    
    setSimulationState(prev=> ({...prev, isRunning: false}))
  };

/** Get the current step in the tree based on the path
   * @returns the step object. if not found - returns null
   */
  const getCurrentStep = () => {
    return getStepFromPath(currentState.stepTree, currentState.currentPath);
  };

  /** Get the next step based on the current path
   * @returns {
   *  * step: the next step object,
   *  * path: the path of the next step,
   *  * exiting: boolean to indicate whether the next step is still in the current submachine or there is a need to exit it
   *  * removeLevels: the num of submachines to exit
   * }
   */
  const getNextStep = () => {
    return getNextStepFromPath(currentState.stepTree, currentState.currentPath);
  };
;

  // Step forward - get next step and apply it
  const stepForward = () => {
    const nextStepInfo = getNextStep();
    
    if (nextStepInfo) {
      if (nextStepInfo.exiting) {
        // Handle exiting submachine - trigers the useeffect
        setCurrentState(prev => ({
          ...prev,
          submachineNextStep: nextStepInfo
        }));
      } else {
        // Move to next step
        setCurrentState(prev => ({
          ...prev,
          currentPath: nextStepInfo.path,
          stepHistory: [...prev.stepHistory, prev.currentPath]
        }));
        
        // Apply the next step
        if (nextStepInfo.step) {
          if (nextStepInfo.step.action === 'submachine' && nextStepInfo.step.steps && nextStepInfo.step.steps.length > 0) {
            enterSubmachine(nextStepInfo.step);
          } else {
            applyStep(nextStepInfo.step);
          }
        }
      }
    }
  };

 

  // Handle submachine next step effects
  useEffect(() => {
    if (currentState.submachineNextStep?.exiting) {
      exitSubmachine(currentState.submachineNextStep);
    }
  }, [currentState.submachineNextStep]);
  

    const waitingInterval = useRef(null);



// Handle animation for current steps
// each step iteration it handles each type of step: for submachine it calls enterSubmachine and for all the others, applyStep knows how to handle
useEffect(() => {
  const currentStep = getCurrentStep();
  const nextStepInfo = getNextStep();

  const advanceToNextStep = () => {
    if (nextStepInfo) {
      // if reached the end of submachine we set submachineNextStep with the step after the submachine to trigger the useeffect and exiting the submachine
      if (nextStepInfo.exiting) {
        setCurrentState(prev => ({
          ...prev,
          submachineNextStep: nextStepInfo
        }));
      } else {
        // Move to next step (in a submachine) - this trigers that useEffect again to set the next step and keep the flow
        setCurrentState(prev => ({
          ...prev,
          currentPath: nextStepInfo.path,
          // Add current path to history for step back
          stepHistory: [...prev.stepHistory, prev.currentPath]
        }));
      }
    } else {
      // if there isn't next step in the tree - wait for chunks to be fetched while !isFinished
      if (!isFinished && !waitingInterval.current) {
        // Start polling for new chunks
        waitingInterval.current = setInterval(() => {
          const retryNextStep = getNextStep();
          if (retryNextStep) {
            clearInterval(waitingInterval.current);
            waitingInterval.current = null;

            if (retryNextStep.exiting) {
              setCurrentState(prev => ({
                ...prev,
                submachineNextStep: retryNextStep
              }));
            } else {
              setCurrentState(prev => ({
                ...prev,
                currentPath: retryNextStep.path,
                stepHistory: [...prev.stepHistory, prev.currentPath]
              }));
            }
          }
        }, 100); // Poll every 100ms
      } else {
        // End of simulation - stay on current step, don't clear anything
        console.log("finished");

        setCurrentState(prev => ({ ...prev, animating: false }));
        setSimulationState(prev => ({ ...prev, isRunning: false }));
      }
    }
  };

  

  // Handle animation for current steps
  // each step iteration it handles each type of step: for submachine it calls enterSubmachine and for all the others, applyStep knows how to handle
  if (currentState.animating && isRunning && currentStep) {
    // Handle submachine steps
    if (currentStep.action === 'submachine' && currentStep.steps && currentStep.steps.length > 0) {
      enterSubmachine(currentStep);
      return;
    }

    // Apply step
    applyStep(currentStep);

    // Delay if it's a 'step' action, otherwise advance immediately
    if (currentStep.action === 'step') {
      animationTimeout.current = setTimeout(() => {
        advanceToNextStep();
      }, currentStep.write?.length > 0 ? stepDuration.current * 1.5 : stepDuration.current);
    } else {
      advanceToNextStep();
      
    }

    return () => {
      if (animationTimeout.current) {
        clearTimeout(animationTimeout.current);
        animationTimeout.current = null;
      }
    };
  }
}, [currentState.currentPath, currentState.animating]);

// console.log(currentState.tapes)

  // Rendering the current state of the Turing machine
  return (
    <div className="turing-machine">
      {/* Display main formula at all times */}
      <div className="mb-2 text-sm font-medium text-gray-700 bg-gray-50 p-2 rounded-md">
        <p className="font-semibold">Main: {currentState.mainFormula}</p>
      </div>
      
      {/* Render active submachines - as a stack of windows */}
      {currentState.activeSubmachines.length > 0 ? (
        <SubmachineStack 
          activeSubmachines={currentState.activeSubmachines} 
          getCurrentStep={getCurrentStep}
          transitionState={currentState.transitionState}
        />
      ) : (
        <>
          {/* Show current step formula if different from submachine */}
          {/*TODO: i didn't understand */}
          {getCurrentFormula(currentState, getCurrentStep) !== currentState.mainFormula && 
           getCurrentStep()?.formula && (
            <div className="mb-2 text-sm font-mono bg-purple-50 p-2 rounded-md">
              <span className="font-medium">Current Operation: </span>
              {getCurrentStep()?.formula}
            </div>
          )}
          
          {/* Render current tapes if no submachines are active */}
          <MainMachineTapes 
            tapes={currentState.tapes}
            transitionState={currentState.transitionState}
            getCurrentStep={getCurrentStep}
          />
        </>
      )}
      
    </div>
  );
});

export default TuringMachine;
