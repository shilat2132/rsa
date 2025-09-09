import GeneralPage from './GeneralPage';

const KeyGeneration = () => {
  const resultsRenderer = (results) => {
    if (!results) return null;

    return (
      <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
        <h3 className="text-lg font-semibold text-green-800 mb-2">
          Key Generation Complete
        </h3>
        <div className="space-y-2">
          <p><strong>Public Key (n):</strong> {results.n} -{">"} {results.resLists.n}</p>
          <p><strong>Private Exponent (a):</strong> {results.a} -{">"} {results.resLists.a}</p>
        </div>
      </div>
    );
  };

  return (
    <GeneralPage
      stage="keyGeneration"
      title="Key Generation"
      subtitle="Generate RSA keys from primes"
      initialInputs={{ p: '', q: '' }}
      resultsRenderer={resultsRenderer}
    />
  );
};

export default KeyGeneration;

