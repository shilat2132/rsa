
import React from 'react';
import TuringTape from './TuringTape';

/**
 * Renders the main machine tapes (when no submachines are active)
 */
const MainMachineTapes = ({ tapes, transitionState, getCurrentStep }) => {
  return (
    <div className="tapes-container space-y-6">
      {tapes.map((tape, index) => (
        <TuringTape
          key={`tape-${index}`}
          tape={tape}
          headPosition={
            transitionState?.positions?.[index] !== undefined ?
            transitionState.positions[index] :
            getCurrentStep()?.pos?.[index]
          }
          tapeIndex={index}
        />
      ))}
    </div>
  );
};

export default MainMachineTapes;
