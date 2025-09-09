
import { Progress } from '@/components/ui/progress';

/**
 * Shows progress of chunks loaded vs total chunks
 */
const LoadingProgress = ({ chunksLoaded, totalChunks, isFinished }) => {
  // Calculate progress percentage
  const progress = totalChunks > 0 
    ? Math.min(Math.round((chunksLoaded / totalChunks) * 100), 100)
    : 0;
  
  // Don't show progress if no chunks loaded yet
  if (chunksLoaded === 0) return null;

  return (
    <div className="mb-6">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm text-gray-500">
          {isFinished ? 'Chunks fetch completed' : 'Loading simulation chunks...'}
        </span>
        <span className="text-sm font-medium">
          {chunksLoaded} / {totalChunks || '?'} chunks
        </span>
      </div>
      <Progress value={progress} className="h-1.5 bg-blue-100">
        <div 
          className="h-full bg-blue-500 transition-all duration-500 ease-in-out" 
          style={{ width: `${progress}%` }}
        ></div>
      </Progress>
    </div>
  );
};

export default LoadingProgress;
