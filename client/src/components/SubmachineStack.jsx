
import TuringTape from './TuringTape';
import styles from '../styles/submachine.module.css';

/**
 * Renders a stack of active submachines
 */
const SubmachineStack = ({ activeSubmachines, getCurrentStep, transitionState }) => {
  return (
    <div className={styles.submachineStack}>
      {activeSubmachines.map((submachine, index) => {
        const isTopLevel = index === activeSubmachines.length - 1;
        
        return (
          <div 
            key={`submachine-${index}`} 
            className={`${styles.submachineWindow} ${isTopLevel ? styles.topLevel : styles.background}`}
            style={{
              transform: isTopLevel ? 'none' : `translateY(${-10 * (activeSubmachines.length - index - 1)}px)`,
              opacity: isTopLevel ? 1 : Math.max(0.2, 1 - ((activeSubmachines.length - index) * 0.2)),
            }}
          >
            <div className={styles.submachineHeader}>
                  <span className={styles.badge}>
                    Submachine Level {submachine.level}
                  </span>
                  {submachine.formula && (
                    <span className={styles.formula}>{submachine.formula}</span>
                  )}
                </div>

            
            {/* Only render tapes for the top-level submachine */}
            {isTopLevel && (
              <div className={styles.tapesContainer}>
                {submachine.tapes && submachine.tapes.map((tape, tapeIndex) => (
                  <TuringTape
                    key={`submachine-${index}-tape-${tapeIndex}`}
                    tape={tape}
                    headPosition={
                      transitionState?.positions?.[tapeIndex] !== undefined ?
                      transitionState.positions[tapeIndex] :
                      getCurrentStep()?.pos?.[tapeIndex]
                    }
                    tapeIndex={tapeIndex}
                  />
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default SubmachineStack;
