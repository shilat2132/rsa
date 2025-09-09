import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import styles from '../styles/InputForm.module.css';
import '../styles/general.css'


const InputForm = ({ stage, onSubmit, error }) => {
  const [formData, setFormData] = useState({});
  const [storageData, setStorageData] = useState({});
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    const keyData = JSON.parse(localStorage.getItem('keys') || '{}');

    if (stage === 'encryption') {
      setStorageData({ b: keyData.b, n: keyData.n });
    } else if (stage === 'decryption') {
      setStorageData({
        a: keyData.a,
        n: keyData.n,
        p: keyData.p,
        q: keyData.q
      });
    } else {
      setStorageData({});
    }

    setFormData({});
    setValidationErrors({});
  }, [stage]);

  const validateField = (name, value) => {
    if (value === '' || isNaN(value) || parseInt(value) < 1) {
      return `${name} must be a number greater than or equal to 1`;
    }

    if (name === 'x' && storageData.n && parseInt(value) >= parseInt(storageData.n)) {
      return `Message (x) must be less than n (${storageData.n})`;
    }

    if (name === 'y' && storageData.n && parseInt(value) >= parseInt(storageData.n)) {
      return `Ciphertext (y) must be less than n (${storageData.n})`;
    }

    return null;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (value === '' || /^\d+$/.test(value)) {
      setFormData(prev => ({ ...prev, [name]: value }));
      const error = validateField(name, value);
      setValidationErrors(prev => ({ ...prev, [name]: error }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newErrors = {};
    let hasErrors = false;

    Object.entries(formData).forEach(([name, value]) => {
      const error = validateField(name, value);
      if (error) {
        newErrors[name] = error;
        hasErrors = true;
      }
    });

    setValidationErrors(newErrors);

    if (hasErrors) {
      toast.error("Please fix the validation errors before submitting.");
      return;
    }

    onSubmit(stage, {
      ...formData,
      ...storageData
    });
  };

  const isSubmitEnabled = () => {
    if (Object.values(validationErrors).some(error => error !== null)) {
      return false;
    }

    if (stage === 'keyGeneration') {
      return formData.p && formData.q && formData.b;
    }
    if (stage === 'encryption') {
      return formData.x && storageData.b && storageData.n;
    }
    if (stage === 'decryption') {
      return formData.y && storageData.a && storageData.n && storageData.p && storageData.q;
    }
    return false;
  };

  const renderFormFields = () => {
    if (stage === 'keyGeneration') {
      return ['p', 'q', 'b'].map(field => (
        <div key={field} className={styles.inputWrapper}>
          <label htmlFor={field} className="block text-sm font-medium text-gray-700">
            {field}
          </label>
          <Input
            id={field}
            name={field}
            type="text"
            value={formData[field] || ''}
            onChange={handleChange}
            placeholder={`Enter ${field}`}
            className={`mt-1 ${styles.inputField} ${validationErrors[field] ? 'border-red-500' : ''}`}
          />
          {validationErrors[field] && (
            <p className="mt-1 text-sm text-red-600">{validationErrors[field]}</p>
          )}
        </div>
      ));
    }

    if (stage === 'encryption') {
      return (
        <div className={styles.inputWrapper}>
          <label htmlFor="x" className="block text-sm font-medium text-gray-700">
            Message (x)
          </label>
          <Input
            id="x"
            name="x"
            type="text"
            value={formData.x || ''}
            onChange={handleChange}
            placeholder="Enter message to encrypt"
            className={`mt-1 ${styles.inputField} ${validationErrors.x ? 'border-red-500' : ''}`}
          />
          {validationErrors.x && (
            <p className="mt-1 text-sm text-red-600">{validationErrors.x}</p>
          )}
        </div>
      );
    }

    if (stage === 'decryption') {
      return (
        <div className={styles.inputWrapper}>
          <label htmlFor="y" className="block text-sm font-medium text-gray-700">
            Ciphertext (y)
          </label>
          <Input
            id="y"
            name="y"
            type="text"
            value={formData.y || ''}
            onChange={handleChange}
            placeholder="Enter ciphertext to decrypt"
            className={`mt-1 ${styles.inputField} ${validationErrors.y ? 'border-red-500' : ''}`}
          />
          {validationErrors.y && (
            <p className="mt-1 text-sm text-red-600">{validationErrors.y}</p>
          )}
        </div>
      );
    }

    return null;
  };

  const buttonText = {
    keyGeneration: 'Generate Keys',
    encryption: 'Encrypt',
    decryption: 'Decrypt'
  };

  const showKeysWarning = (stage === 'encryption' || stage === 'decryption') &&
    (!storageData.n || (stage === 'encryption' && !storageData.b) ||
      (stage === 'decryption' && !storageData.a));

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.formSection}>
        {showKeysWarning && (
          <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg mb-4">
            <p className="text-sm text-yellow-700">
              You must generate RSA keys before you can {stage === 'encryption' ? 'encrypt' : 'decrypt'} messages.
            </p>
            <Button
              variant="link"
              className="text-blue-600 p-0 h-auto font-medium"
              onClick={() => window.location.href = '/key-generation'}
            >
              Go to Key Generation
            </Button>
          </div>
        )}

        {renderFormFields()}

        {error && <p className='errMsg'>{error.message || "Something went wrong"} </p>}
        <div className={styles.buttonWrapper}>
          <Button
            type="submit"
            disabled={!isSubmitEnabled() || showKeysWarning}
            className={styles.submitButton}
          >
            {buttonText[stage] || 'Submit'}
          </Button>
        </div>
      </form>

      {!showKeysWarning && (stage === 'encryption' || stage === 'decryption') && (
        <div className={styles.card}>
          <div className={styles.cardTitle}>RSA {stage === 'encryption' ? "public" : "private"} Keys</div>
          {Object.entries(storageData).map(([key, value]) => (
            <div key={key} className={styles.cardItem}>
              <strong>{key}:</strong> {value || 'N/A'}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default InputForm;
