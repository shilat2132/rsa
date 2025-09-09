import { Button } from '@/components/ui/button';
import {
  Play,
  Pause,
  StepForward,
  RefreshCw
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

/**
 * Controls for the simulation (play/pause, step forward, speed)
 */
const SimulationControls = ({
  isRunning,
  onPlayPause,
  onStepForward,
  onRestart,
  speed = 1,
  onSpeedChange
}) => {
  const handleSpeedChange = (value) => {
    if (onSpeedChange) {
      onSpeedChange(Number(value));
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Reset button */}
      {onRestart && (
        <Button
          variant="outline"
          size="icon"
          onClick={onRestart}
          title="Restart"
        >
          <RefreshCw className="h-4 w-4" />
        </Button>
      )}


      {/* Play/Pause button */}
      {onPlayPause && (
        <Button
          variant={isRunning ? "secondary" : "outline"}
          size="icon"
          onClick={onPlayPause}
          title={isRunning ? "Pause" : "Play"}
        >
          {isRunning ? (
            <Pause className="h-4 w-4" />
          ) : (
            <Play className="h-4 w-4" />
          )}
        </Button>
      )}

      {/* Step forward button */}
      {onStepForward && (
        <Button
          variant="outline"
          size="icon"
          onClick={onStepForward}
          title="Step Forward"
        >
          <StepForward className="h-4 w-4" />
        </Button>
      )}

      {/* Speed selector */}
      {onSpeedChange && (
        <div className="ml-2">
          <Select
            value={speed.toString()}
            onValueChange={handleSpeedChange}
          >
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Speed" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="0.5">0.5x</SelectItem>
              <SelectItem value="1">1x</SelectItem>
              <SelectItem value="1.5">1.5x</SelectItem>
              <SelectItem value="2">2x</SelectItem>
              <SelectItem value="2.5">2.5x</SelectItem>
              <SelectItem value="3">3x</SelectItem>
              <SelectItem value="3.5">3.5x</SelectItem>
              <SelectItem value="4">4x</SelectItem>
            </SelectContent>
          </Select>
        </div>
      )}
    </div>
  );
};

export default SimulationControls;
