import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import MainNavigation from '../components/MainNavigation';
import HomeHeader from '../components/HomeHeader';
import styles from '../styles/homepage.module.css';

const HomePage = () => {
  const [hasKeys, setHasKeys] = useState(false);

  useEffect(() => {
    const keys = JSON.parse(localStorage.getItem('keys') || '{}');
    setHasKeys(keys && keys.n && keys.b && keys.a);
  }, []);

  const simulations = [
    {
      title: "Key Generation",
      icon: "🔑",
      description: "Generate public and private RSA keys from prime numbers p and q",
      path: "/key-generation",
      status: "start"
    },
    {
      title: "Encryption",
      icon: "🔒",
      description: "Encrypt messages using the public key (b,n)",
      path: "/encryption",
      status: hasKeys ? "ready" : "needs-keys"
    },
    {
      title: "Decryption",
      icon: "🔓",
      description: "Decrypt ciphertexts using the private key (a,n)",
      path: "/decryption",
      status: hasKeys ? "ready" : "needs-keys"
    }
  ];

  const howItWorksSteps = [
    {
      title: "1. Key Generation",
      description: "Choose two prime numbers p and q, then calculate n = p×q. The public key is (b,n) and the private key is (a,p,q)."
    },
    {
      title: "2. Encryption",
      description: "Using the public key (b,n), encrypt a message x to produce ciphertext y: y = x^b mod n"
    },
    {
      title: "3. Decryption",
      description: "Using the private key (a,n), decrypt the ciphertext y to recover x: x = y^a mod n"
    }
  ];

  const exampleKeySets = [
    { p: 3, q: 11, b: 7 },
    { p: 5, q: 13, b: 3 },
    { p: 7, q: 17, b: 5 },
    { p: 11, q: 17, b: 7 }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.mainContent}>
        <MainNavigation />
        <HomeHeader />

        <div className={styles.twoColumnLayout}>
          <div className={styles.leftColumn}>
            <div className={styles.sectionCard}>
              <h2 className={styles.sectionTitle}>How RSA Works</h2>
              <div className={styles.stepsGrid}>
                {howItWorksSteps.map((step, i) => (
                  <div key={i} className={styles.stepCard}>
                    <h3 className={styles.stepTitle}>{step.title}</h3>
                    <p className={styles.stepDescription}>{step.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.sectionCard}>
              <h2 className={styles.sectionTitle}>Example RSA Key Sets</h2>
              <div className={styles.exampleSetGrid}>
                {exampleKeySets.map((set, i) => (
                  <div key={i} className={styles.exampleCard}>
                    <p><strong>p:</strong> {set.p}</p>
                    <p><strong>q:</strong> {set.q}</p>
                    <p><strong>b:</strong> {set.b}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className={styles.rightColumn}>
            <div className={styles.sectionCard}>
              <h2 className={styles.sectionTitle}>RSA Simulations</h2>
              {simulations.map((sim, i) => (
                <div key={i} className={styles.simulationCard}>
                  <div className={styles.cardHeader}>
                    <span className={styles.simulationIcon}>{sim.icon}</span>
                    {sim.status === 'ready' && <span className={`${styles.statusBadge} ${styles.statusReady}`}>Ready</span>}
                    {sim.status === 'needs-keys' && <span className={`${styles.statusBadge} ${styles.statusNeedsKeys}`}>Needs Keys</span>}
                  </div>
                  <h3 className={styles.simulationTitle}>{sim.title}</h3>
                  <p className={styles.simulationDescription}>{sim.description}</p>
                  <Link
                    to={sim.path}
                    className={styles.simulationButton}
                    style={{
                      pointerEvents: sim.status === 'needs-keys' ? 'none' : 'auto',
                      opacity: sim.status === 'needs-keys' ? 0.6 : 1
                    }}
                  >
                    {sim.status === 'start' ? 'Start' : sim.status === 'ready' ? 'Continue' : 'Requires Keys'}
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
