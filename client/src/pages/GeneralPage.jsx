import { useState, useEffect, useRef } from 'react';

import SimulationControls from '../components/SimulationControls';
import InputForm from '../components/InputForm';
import TuringMachine from '../components/TuringMachine';
import LoadingProgress from '../components/LoadingProgress';
import MainNavigation from '../components/MainNavigation';
import { fetchInitialSimulation, fetchNextChunk } from '../utils/api';
import { processChunk, getNextStepPath } from '../utils/operations/simulationProcessor';

const GeneralPage = ({
  stage,
  resultsRenderer = null
}) => {
  // Simulation state
  const [simulationState, setSimulationState] = useState({
    stage,
    mainStep: null,
    stepTree: {},
    isRunning: false,
    currentStepPath: [],
    speed: 1,
    chunksLoaded: 0,
    totalChunks: 100, // Default estimate, will be updated from API
    isFinished: false,
    isFetching: false,
    hasStarted: false
  });

  // Results (to store values and pass to the next stage)
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null)
  // Reference to the TuringMachine component
  const turingMachineRef = useRef(null);

  // Handle form submission
  const handleSubmit = async (stage, formData) => {
    try {
      setError(null)
      setResults(null)
      // Reset simulation state
      setSimulationState(prev => ({
        ...prev,
        mainStep: null,
        stepTree: {},
        isRunning: false,
        currentStepPath: [],
        chunksLoaded: 0,
        isFinished: false,
        isFetching: true,
        hasStarted: false
      }));

      


      // Fetch initial simulation data
      const initialData = await fetchInitialSimulation(stage, formData);
      
      // Process initial data
      const mainStep = initialData.main_step;
      const stepTree = { steps: [mainStep] };

      // Update simulation state with initial data
      setSimulationState(prev => ({
        ...prev,
        mainStep,
        stepTree,
        chunksLoaded: 0,
        totalChunks: initialData.total_chunks || 100, // Use API value or default
        isFinished: false,
        isFetching: false,
        hasStarted: true,
        currentStepPath: [0] // Initialize with the path to the main step
      }));

      // Store results if available
      if (initialData.results) {
        setResults(initialData.results);
        if(stage === "keyGeneration"){
          const {resLists, ...resultsNums} = initialData.results
          localStorage.setItem(`keys`, JSON.stringify(resultsNums));
        }
      }

      // Prefetch first few chunks
      await prefetchChunks(stage, 3);
    } catch (error) {
      setSimulationState(prev => ({
        ...prev,
        isFinished: false,
        isFetching: false,
      
      }));
      setError(error)
      setResults(null)
    }
  };

  /** Prefetch multiple chunks - not the full tree, just the first chunks */
  const prefetchChunks = async (stage, count) => {
    for (let i = 0; i < count; i++) {
      const hasMore = await fetchChunk(stage);
      if (!hasMore) break;
    }
  };

  /** Fetch a single chunk and inserts it in the tree
   * @param stage: 'keyGeneration', 'encryption', or 'decryption' for the api request
   * @returns boolean - whether there are more chunks to be sent afterward
   */
  const fetchChunk = async (stage) => {
    if (simulationState.isFinished || simulationState.isFetching) {
      return false;
    }

    try {
      setSimulationState(prev => ({ ...prev, isFetching: true }));

      const response = await fetchNextChunk(stage);

      if (!response || !response.chunk) {
        setSimulationState(prev => ({
          ...prev,
          isFinished: true,
          isFetching: false
        }));
        return false;
      }

      setSimulationState(prev => {
        // Process the new chunk and update step tree
        const updatedTree = processChunk(prev.stepTree, response.chunk);
        return {
          ...prev,
          stepTree: updatedTree,
          chunksLoaded: response.chunk.length > 0  ? prev.chunksLoaded + 1 : prev.chunksLoaded,
          isFinished: response.finished || false,
          isFetching: false
        };
      });

      return !response.finished;

    } catch (error) {
      setError(error)
      setSimulationState(prev => ({ ...prev, isFetching: false, isRunning: false }));
      return false;
    }
  };

  // Toggle simulation running state
  const togglePlayPause = () => {
    setSimulationState(prev => ({ 
      ...prev, 
      isRunning: !prev.isRunning 
    }));
  };

  // Restart simulation - complete reset to initial state
  const handleRestart = () => {
    if (!simulationState.mainStep) return;
    
    // Use TuringMachine's restart method to properly reset everything
    if (turingMachineRef.current && typeof turingMachineRef.current.handleFullRestart === 'function') {
      turingMachineRef.current.handleFullRestart();
    }
    
    setSimulationState(prev => ({
      ...prev,
      isRunning: false,
      currentStepPath: [0], // Reset to the first step
    }));
  };

  // Step forward using TuringMachine's method
  const stepForward = () => {
    if (turingMachineRef.current && typeof turingMachineRef.current.stepForward === 'function') {
      turingMachineRef.current.stepForward();
    } else {
      // Fallback to previous behavior
      const { stepTree, currentStepPath } = simulationState;

      if (!currentStepPath || currentStepPath.length === 0) {
        setSimulationState(prev => ({
          ...prev,
          currentStepPath: [0]
        }));
        return;
      }

      const nextPath = getNextStepPath(stepTree, currentStepPath);

      if (nextPath) {
        setSimulationState(prev => ({
          ...prev,
          currentStepPath: nextPath
        }));
      } else {
        fetchChunk(simulationState.stage).then(hasMore => {
          if (!hasMore) {
            console.log('End of simulation reached');
          }
        });
      }
    }
  };
  


  // Change simulation speed
  const changeSpeed = (newSpeed) => {
    setSimulationState(prev => ({ ...prev, speed: newSpeed }));
  };

  // Prefetch more chunks when needed
  useEffect(() => {
    if (simulationState.mainStep && !simulationState.isFinished) {
      if (simulationState.chunksLoaded > 0 && simulationState.chunksLoaded % 3 === 0) {
        prefetchChunks(simulationState.stage, 3);

      }
    }
  }, [simulationState.chunksLoaded]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-purple-50">
      <div className="container mx-auto px-4 py-10">
        <MainNavigation />

        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 capitalize">
            {stage.replace(/([A-Z])/g, ' $1')}
          </h1>
          <p className="text-lg text-gray-600">
            Simulate RSA {stage} using Turing Machines
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Section */}
          <div className="lg:col-span-1 bg-white rounded-lg p-6 shadow-md">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Parameters</h2>
            <InputForm
              stage={stage}
              onSubmit={handleSubmit}
              error={error}
            />

            {/* Render results */}
            { results && (
              <div className="mt-6 p-4 bg-purple-50 rounded-lg border border-purple-200">
                {resultsRenderer ? resultsRenderer(results) : (
                  <div>
                    <h3 className="text-lg font-semibold text-purple-800 mb-2">Simulation Complete</h3>
                    <p className="text-gray-700">Results ready. Implement `resultsRenderer` to customize.</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Simulation Section */}
          <div className="lg:col-span-2 bg-white rounded-lg p-6 shadow-md">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold text-gray-800">
                {stage.charAt(0).toUpperCase() + stage.slice(1)} Simulation
              </h2>
              
              {simulationState.hasStarted && <SimulationControls
                isRunning={simulationState.isRunning}
                onPlayPause={togglePlayPause}
                onStepForward={stepForward}
                onRestart={handleRestart}
               
                speed={simulationState.speed}
                onSpeedChange={changeSpeed}
              />}
            </div>

            {/* Progress indicator */}
            <LoadingProgress
              chunksLoaded={simulationState.chunksLoaded}
              totalChunks={simulationState.totalChunks}
              isFinished={simulationState.isFinished}
            />

            {/* Turing Machine Visualization */}
            {simulationState.mainStep ? (
              <TuringMachine
                ref={turingMachineRef}
                isFinished = {simulationState.isFinished}
                stepTree={simulationState.stepTree}
                isRunning={simulationState.isRunning}
                setSimulationState = {setSimulationState}
                speed={simulationState.speed}
                currentPath={simulationState.currentStepPath}
              />
            ) : (
              <div className="flex items-center justify-center h-60">
                <p className="text-gray-500">
                  {simulationState.isFetching ?
                    "Setting up simulation..." :
                    "Enter parameters and click Submit to start the simulation"}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneralPage;
