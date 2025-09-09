
import { useState, useRef, useEffect } from 'react';
import styles from '../styles/turingTape.module.css';

/**
 * Renders a single Turing machine tape with animated head
 */
const TuringTape = ({ tape, headPosition, tapeIndex }) => {
  if(!headPosition) headPosition = 0
  
  const scrollRef = useRef(null);
  const [visibleCells, setVisibleCells] = useState([]);

  // Calculate visible portion of tape whenerver its head or content change
  useEffect(() => {
    if (!tape) return;
    
    // Ensure we show at least 70 cells, centered on the head position
    const minVisible = 30
    const currentHead = headPosition !== null ? headPosition : 0;
    const startIdx = Math.max(0, currentHead - Math.floor(minVisible / 2)); //the start index from which to show the tape
    
    // Calculate visible range based on tape length
    let visibleRange = [];
    for (let i = startIdx; i < Math.min(tape.length, startIdx + minVisible); i++) {
      visibleRange.push({ value: tape[i], index: i });
    }
    
    // Pad with empty cells if needed
    while (visibleRange.length < minVisible) {
      if (startIdx > 0 && visibleRange.length < minVisible) {
        // Add at start
        visibleRange.unshift({ value: '_', index: -1 });
      } else {
        // Add at end
        visibleRange.push({ value: '_', index: tape.length + (visibleRange.length - (tape.length - startIdx)) });
      }
    }
    
    setVisibleCells(visibleRange);
  }, [tape, headPosition]);

  // Scroll to ensure head position is visible
  useEffect(() => {
    if (scrollRef.current && headPosition !== null) {
      const headElement = document.getElementById(`tape-${tapeIndex}-cell-${headPosition}`);
      if (headElement) {
        const containerRect = scrollRef.current.getBoundingClientRect();
        const headRect = headElement.getBoundingClientRect();
        
        const isInView = 
          headRect.left >= containerRect.left &&
          headRect.right <= containerRect.right;
        
        if (!isInView) {
          // Scroll to head with some padding
          const scrollPosition = 
            headElement.offsetLeft - 
            scrollRef.current.offsetLeft - 
            (scrollRef.current.offsetWidth / 2) + 
            (headElement.offsetWidth / 2);
            
          scrollRef.current.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
          });
        }
      }
    }
  }, [headPosition, visibleCells, tapeIndex]);
// console.log(tapeIndex, tape)
  return (
    <div className={styles.tapeWrapper}>
      <div className={styles.tapeLabel}>Tape {tapeIndex + 1}</div>
      
      <div className={styles.tapeContainer} ref={scrollRef}>
        <div className={styles.tape}>
          {visibleCells.map((cell, idx) => (
            <div 
              key={`cell-${idx}`}
              id={cell.index >= 0 ? `tape-${tapeIndex}-cell-${cell.index}` : undefined}
              className={`${styles.cell} ${
                cell.index === headPosition ? styles.cellActive : ''
              }`}
            >
              {cell.value}
            </div>
          ))}
        </div>
      </div>
      
      <div className={styles.headIndicators}>
        {visibleCells.map((cell, idx) => (
          <div 
            key={`head-${idx}`}
            className={`${styles.headIndicator} ${
              cell.index === headPosition ? styles.headIndicatorActive : styles.headIndicatorInvisible
            }`}
          >
            ▲
          </div>
        ))}
      </div>
    </div>
  );
};

export default TuringTape;
