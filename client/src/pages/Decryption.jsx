
import { useState, useEffect } from 'react';
import GeneralPage from './GeneralPage';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { useNavigate, useLocation } from 'react-router-dom';

const Decryption = () => {
  const [keys, setKeys] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const [initialValue, setInitialValue] = useState('');
  
  useEffect(() => {
    // Load keys from localStorage
    const storedKeys = JSON.parse(localStorage.getItem('keys') || '{}');
    if (storedKeys && storedKeys.a && storedKeys.n && storedKeys.p && storedKeys.q) {
      setKeys(storedKeys);
    }
    
    // Check if we have a y value from navigation
    if (location.state?.y) {
      setInitialValue(location.state.y);
    }
  }, [location]);

  const resultsRenderer = (results) => {
    if (!results) return null;

    return (
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">Decryption Complete</h3>
        <div className="space-y-2">
          <p><strong>Encrypted Message (y):</strong> {results?.y} -{">"} {results.resLists.y}</p>
          <p><strong>Decrypted Message (x):</strong> {results?.x} -{">"} {results.resLists.x}</p>
        </div>
        
        <Button 
          onClick={() => navigate('/')}
          className="mt-4 w-full bg-blue-500 hover:bg-blue-600"
        >
          Back to Home
        </Button>
      </div>
    );
  };

  const renderKeysInfo = () => {
    if (!keys) {
      return (
        <Alert variant="warning" className="mb-4 bg-yellow-50 border-yellow-300">
          <AlertTitle className="text-yellow-800">No RSA Keys Found</AlertTitle>
          <AlertDescription className="text-yellow-700">
            You need to generate RSA keys before decrypting messages.
            <Button 
              variant="link" 
              onClick={() => navigate('/key-generation')}
              className="p-0 h-auto font-medium text-blue-600 ml-2"
            >
              Generate Keys
            </Button>
          </AlertDescription>
        </Alert>
      );
    }

    return (
      <Alert className="mb-4 bg-blue-50 border-blue-200">
        <AlertTitle className="text-blue-800">Using RSA Private Key</AlertTitle>
        <AlertDescription className="text-blue-700">
          <p><strong>n:</strong> {keys.n}</p>
          <p><strong>a:</strong> {keys.a}</p>
          <p><strong>p:</strong> {keys.p}</p>
          <p><strong>q:</strong> {keys.q}</p>
          <Button 
            variant="link" 
            onClick={() => navigate('/key-generation')}
            className="p-0 h-auto font-medium text-blue-600"
          >
            Generate New Keys
          </Button>
        </AlertDescription>
      </Alert>
    );
  };

  return (
    <GeneralPage
      stage="decryption"
      title="Decryption"
      subtitle="Decrypt a message (y) using RSA"
      initialInputs={{ y: initialValue }}
      resultsRenderer={resultsRenderer}
      additionalContent={renderKeysInfo()}
      nextStepLabel="Back to Home"
      nextStepPath="/"
    />
  );
};

export default Decryption;
