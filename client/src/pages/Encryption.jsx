
import { useState, useEffect } from 'react';
import GeneralPage from './GeneralPage';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';

const Encryption = () => {
  const [keys, setKeys] = useState(null);
  const navigate = useNavigate();
  
  useEffect(() => {
    // Load keys from localStorage
    const storedKeys = JSON.parse(localStorage.getItem('keys') || '{}');
    if (storedKeys && storedKeys.b && storedKeys.n) {
      setKeys(storedKeys);
    }
  }, []);

  const resultsRenderer = (results) => {
    if (!results) return null;

    return (
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">Encryption Complete</h3>
        <div className="space-y-2">
          <p><strong>Original Message (x):</strong> {results?.x} -{">"} {results.resLists.x} </p>
          <p><strong>Encrypted Message (y):</strong> {results.y} -{">"} {results.resLists.y}</p>
        </div>
        
        <Button 
          onClick={() => navigate('/decryption', { state: { y: results.y } })}
          className="mt-4 w-full bg-blue-500 hover:bg-blue-600"
        >
          Continue to Decryption
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
            You need to generate RSA keys before encrypting messages.
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
        <AlertTitle className="text-blue-800">Using RSA Public Key</AlertTitle>
        <AlertDescription className="text-blue-700">
          <p><strong>n:</strong> {keys.n}</p>
          <p><strong>b:</strong> {keys.b}</p>
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
      stage="encryption"
      title="Encryption"
      subtitle="Encrypt a message (x) using RSA"
      initialInputs={{ x: '' }}
      resultsRenderer={resultsRenderer}
      additionalContent={renderKeysInfo()}
      nextStepLabel="Continue to Decryption"
      nextStepPath="/decryption"
    />
  );
};

export default Encryption;
